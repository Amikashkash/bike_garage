from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import RepairJob, CustomerNotification, Customer
from .views import is_manager, is_mechanic, is_customer
import json


@login_required
@require_http_methods(["GET"])
def manager_stats(request):
    """API endpoint for manager dashboard statistics"""
    if not is_manager(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    from django.db.models import Sum
    from datetime import timedelta
    
    # Basic counts
    pending_diagnosis_count = RepairJob.objects.filter(status='reported').count()
    pending_approval_count = RepairJob.objects.filter(status='diagnosed').count()
    in_progress_count = RepairJob.objects.filter(status='in_progress').count()
    blocked_tasks_count = RepairJob.objects.filter(is_stuck=True).count()
    ready_for_pickup_count = RepairJob.objects.filter(status='quality_approved').count()
    
    
    # Expected revenue from repairs awaiting approval
    expected_revenue = RepairJob.objects.filter(
        status__in=['diagnosed', 'approved_partial', 'approved_full']
    ).aggregate(
        total=Sum('repair_items__price')
    )['total'] or 0
    
    # Workshop efficiency (percentage of repairs completed this week)
    week_ago = timezone.now() - timedelta(days=7)
    
    total_repairs_week = RepairJob.objects.filter(created_at__gte=week_ago).count()
    completed_week = RepairJob.objects.filter(
        created_at__gte=week_ago,
        status__in=['quality_approved', 'delivered', 'completed']
    ).count()
    
    efficiency = int((completed_week / total_repairs_week * 100)) if total_repairs_week > 0 else 0
    
    # Additional weekly stats - Customer model doesn't have created_at field
    # Count customers who had their first repair this week instead
    new_customers_this_week = Customer.objects.filter(
        bikes__repairjob__created_at__gte=week_ago
    ).distinct().count()
    
    # Revenue this week (completed repairs)
    revenue_this_week = RepairJob.objects.filter(
        updated_at__gte=week_ago,
        status__in=['quality_approved', 'delivered', 'completed']
    ).aggregate(
        total=Sum('repair_items__price')
    )['total'] or 0
    
    # User info
    user_data = {
        'username': request.user.username,
        'full_name': request.user.get_full_name() if request.user.get_full_name() else None,
    }
    
    response_data = {
        'pending_diagnosis_count': pending_diagnosis_count,
        'pending_approval_count': pending_approval_count,
        'in_progress_count': in_progress_count,
        'blocked_tasks_count': blocked_tasks_count,
        'ready_for_pickup_count': ready_for_pickup_count,
        'expected_revenue': float(expected_revenue),
        'efficiency': efficiency,
        'completed_this_week': completed_week,
        'new_customers_this_week': new_customers_this_week,
        'revenue_this_week': float(revenue_this_week),
        'user': user_data,
        'status': 'success'
    }
    
    
    return JsonResponse(response_data)


@login_required
@require_http_methods(["GET"])
def customer_active_repairs(request):
    """API endpoint for customer's active repairs"""
    if not is_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        customer = Customer.objects.get(user=request.user)
        repairs = RepairJob.objects.filter(
            bike__customer=customer,
            status__in=['reported', 'diagnosed', 'approved', 'in_progress', 
                       'awaiting_quality_check', 'quality_approved']
        )
        
        repair_list = []
        for repair in repairs:
            repair_list.append({
                'id': repair.id,
                'bike_info': f"{repair.bike.brand} {repair.bike.model}",
                'status': repair.status,
                'status_display': repair.get_status_display(),
                'progress': repair.progress_percentage,
                'created_at': repair.created_at.isoformat() if repair.created_at else None
            })
        
        return JsonResponse({
            'repairs': repair_list,
            'count': len(repair_list),
            'status': 'success'
        })
        
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def customer_notifications(request):
    """API endpoint for customer notifications count"""
    if not is_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        customer = Customer.objects.get(user=request.user)
        unread_count = CustomerNotification.objects.filter(
            customer=customer,
            is_read=False
        ).count()
        
        return JsonResponse({
            'unread_count': unread_count,
            'status': 'success'
        })
        
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def customer_notifications_list(request):
    """API endpoint for customer notifications list"""
    if not is_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        customer = Customer.objects.get(user=request.user)
        notifications = CustomerNotification.objects.filter(
            customer=customer
        ).order_by('-created_at')[:20]  # Last 20 notifications
        
        notification_list = []
        for notification in notifications:
            notification_list.append({
                'notification_id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'notification_type': notification.notification_type,
                'action_url': notification.action_url,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),
                'repair_id': notification.repair_job.id if notification.repair_job else None
            })
        
        return JsonResponse({
            'notifications': notification_list,
            'status': 'success'
        })
        
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


@login_required 
@require_http_methods(["POST"])
def mark_notification_read(request):
    """API endpoint to mark notification as read"""
    if not is_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        customer = Customer.objects.get(user=request.user)
        notification = get_object_or_404(
            CustomerNotification, 
            id=notification_id, 
            customer=customer
        )
        
        notification.mark_as_read()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Notification marked as read'
        })
        
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
@require_http_methods(["GET"])
def mechanic_stats(request):
    """API endpoint for mechanic statistics"""
    if not is_mechanic(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Count assigned repairs
    assigned_repairs = RepairJob.objects.filter(
        assigned_mechanic=request.user,
        status='in_progress'
    ).count()
    
    # Count completed this week
    from django.utils import timezone
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)
    
    completed_this_week = RepairJob.objects.filter(
        assigned_mechanic=request.user,
        status='awaiting_quality_check',
        updated_at__gte=week_ago
    ).count()
    
    return JsonResponse({
        'assigned_repairs': assigned_repairs,
        'completed_this_week': completed_this_week,
        'status': 'success'
    })


@login_required
@require_http_methods(["POST"])
def report_stuck_repair(request, repair_id):
    """API endpoint for mechanics to report stuck repairs"""
    if not is_mechanic(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        reason = data.get('reason', '').strip()
        
        if not reason:
            return JsonResponse({'error': 'Reason is required'}, status=400)
        
        repair_job = get_object_or_404(RepairJob, id=repair_id, assigned_mechanic=request.user)
        
        if repair_job.status != 'in_progress':
            return JsonResponse({'error': 'Repair is not in progress'}, status=400)
        
        # Mark repair as stuck
        repair_job.is_stuck = True
        repair_job.stuck_reason = reason
        repair_job.stuck_at = timezone.now()
        repair_job.save()
        
        # Real-time notification will be sent by signals
        
        return JsonResponse({
            'status': 'success',
            'message': 'Repair marked as stuck'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
@require_http_methods(["POST"])
def resolve_stuck_repair(request, repair_id):
    """API endpoint for managers to resolve stuck repairs"""
    if not is_manager(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        manager_response = data.get('manager_response', '').strip()
        
        if not manager_response:
            return JsonResponse({'error': 'Manager response is required'}, status=400)
        
        repair_job = get_object_or_404(RepairJob, id=repair_id)
        
        if not repair_job.is_stuck:
            return JsonResponse({'error': 'Repair is not stuck'}, status=400)
        
        # Resolve stuck repair
        repair_job.is_stuck = False
        repair_job.stuck_resolved = True
        repair_job.manager_response = manager_response
        repair_job.resolved_at = timezone.now()
        repair_job.resolved_by = request.user
        repair_job.save()
        
        # Real-time notification will be sent by signals
        
        return JsonResponse({
            'status': 'success',
            'message': 'Stuck repair resolved'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@login_required
@require_http_methods(["GET"])
def manager_dashboard_data(request):
    """API endpoint for manager dashboard data"""
    if not is_manager(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    from django.utils import timezone
    from datetime import timedelta
    
    # Helper function to serialize repair data
    def serialize_repair(repair):
        return {
            'id': repair.id,
            'bike': {
                'brand': repair.bike.brand if repair.bike else '',
                'model': repair.bike.model if repair.bike else '',
                'customer': {
                    'name': repair.bike.customer.name if repair.bike and repair.bike.customer else '',
                    'phone': repair.bike.customer.phone if repair.bike and repair.bike.customer else ''
                }
            },
            'assigned_mechanic': {
                'username': repair.assigned_mechanic.username if repair.assigned_mechanic else None,
                'get_full_name': repair.assigned_mechanic.get_full_name() if repair.assigned_mechanic else None
            } if repair.assigned_mechanic else None,
            'stuck_reason': getattr(repair, 'stuck_reason', ''),
            'progress_percentage': repair.progress_percentage if hasattr(repair, 'progress_percentage') else 0,
            'get_total_price': repair.get_total_price() if hasattr(repair, 'get_total_price') else 0,
            'get_total_approved_price': repair.get_total_approved_price() if hasattr(repair, 'get_total_approved_price') else 0,
            'created_at_display': repair.created_at.strftime('%d/%m %H:%M') if repair.created_at else '',
            'completed_at_display': repair.completed_at.strftime('%d/%m %H:%M') if hasattr(repair, 'completed_at') and repair.completed_at else ''
        }
    
    # Get all repair data
    stuck_repairs = RepairJob.objects.filter(is_stuck=True).select_related('bike', 'bike__customer', 'assigned_mechanic')
    pending_diagnosis = RepairJob.objects.filter(status='reported').select_related('bike', 'bike__customer')
    pending_approval = RepairJob.objects.filter(status='diagnosed').select_related('bike', 'bike__customer')
    approved_waiting_for_mechanic = RepairJob.objects.filter(
        status__in=['approved', 'partially_approved'],
        assigned_mechanic__isnull=True
    ).select_related('bike', 'bike__customer')
    in_progress = RepairJob.objects.filter(status='in_progress').select_related('bike', 'bike__customer', 'assigned_mechanic')
    awaiting_quality_check = RepairJob.objects.filter(status='awaiting_quality_check').select_related('bike', 'bike__customer', 'assigned_mechanic')
    repairs_not_collected = RepairJob.objects.filter(status='quality_approved').select_related('bike', 'bike__customer')
    
    return JsonResponse({
        'stuck_repairs': [serialize_repair(repair) for repair in stuck_repairs],
        'pending_diagnosis': [serialize_repair(repair) for repair in pending_diagnosis],
        'pending_approval': [serialize_repair(repair) for repair in pending_approval],
        'approved_waiting_for_mechanic': [serialize_repair(repair) for repair in approved_waiting_for_mechanic],
        'in_progress': [serialize_repair(repair) for repair in in_progress],
        'awaiting_quality_check': [serialize_repair(repair) for repair in awaiting_quality_check],
        'repairs_not_collected': [serialize_repair(repair) for repair in repairs_not_collected],
        'status': 'success'
    })


@login_required
@require_http_methods(["GET"])
def mechanic_dashboard_data(request):
    """API endpoint for mechanic dashboard data"""
    if not is_mechanic(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Get assigned repairs for this mechanic
    assigned_repairs = RepairJob.objects.filter(
        assigned_mechanic=request.user
    ).select_related('bike', 'bike__customer').prefetch_related('repair_items')
    
    # Calculate statistics based on progress percentage (like the frontend does)
    total_assigned = assigned_repairs.count()
    
    # Count completed repairs by checking progress percentage = 100%
    completed = 0
    stuck = 0
    in_progress = 0
    
    for repair in assigned_repairs:
        # Calculate progress percentage
        completed_items = repair.repair_items.filter(status='completed').count() if hasattr(repair, 'repair_items') else 0
        total_items = repair.repair_items.count() if hasattr(repair, 'repair_items') else 0
        progress_percentage = int((completed_items / total_items * 100)) if total_items > 0 else 0
        
        if repair.is_stuck:
            stuck += 1
        elif progress_percentage == 100:
            completed += 1
        else:
            in_progress += 1
    
    # Helper function to serialize repair data
    def serialize_repair(repair):
        # Calculate progress percentage based on repair items status
        completed_count = repair.repair_items.filter(status='completed').count() if hasattr(repair, 'repair_items') else 0
        total_items_count = repair.repair_items.count() if hasattr(repair, 'repair_items') else 0
        progress_percentage = int((completed_count / total_items_count * 100)) if total_items_count > 0 else 0
        
        return {
            'id': repair.id,
            'bike': {
                'brand': repair.bike.brand if repair.bike else '',
                'model': repair.bike.model if repair.bike else '',
                'customer': {
                    'name': repair.bike.customer.name if repair.bike and repair.bike.customer else '',
                    'phone': repair.bike.customer.phone if repair.bike and repair.bike.customer else ''
                }
            },
            'progress_percentage': progress_percentage,
            'is_stuck': getattr(repair, 'is_stuck', False),
            'stuck_reason': getattr(repair, 'stuck_reason', ''),
            'manager_response': getattr(repair, 'manager_response', ''),
            'diagnosis': getattr(repair, 'diagnosis', ''),
            'created_at': repair.created_at.isoformat() if repair.created_at else '',
            'completed_count': completed_count,
            'pending_count': total_items_count - completed_count,
            'total_items_count': total_items_count,
            'approved_items': [
                {
                    'description': item.description,
                    'price': float(item.price) if item.price else 0,
                    'notes': getattr(item, 'notes', ''),
                    'status': getattr(item, 'status', 'pending')
                } for item in repair.repair_items.filter(is_approved_by_customer=True)
            ] if hasattr(repair, 'repair_items') else []
        }
    
    return JsonResponse({
        'assigned_repairs': [serialize_repair(repair) for repair in assigned_repairs],
        'stats': {
            'total_assigned': total_assigned,
            'completed': completed,
            'in_progress': in_progress,
            'stuck': stuck
        },
        'user_info': {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'full_name': request.user.get_full_name()
        },
        'status': 'success'
    })


@login_required
@require_http_methods(["GET"])
def customer_bikes(request):
    """API endpoint for customer's bikes"""
    if not is_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        customer = Customer.objects.get(user=request.user)
        from .models import Bike
        bikes = Bike.objects.filter(customer=customer)

        bikes_data = [{
            'id': bike.id,
            'brand': bike.brand,
            'model': bike.model,
            'serial_number': bike.serial_number if hasattr(bike, 'serial_number') else None
        } for bike in bikes]

        return JsonResponse(bikes_data, safe=False)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def categories_list(request):
    """API endpoint for repair categories with subcategories"""
    from .models import RepairCategory

    categories = RepairCategory.objects.prefetch_related('subcategories').all()

    categories_data = [{
        'id': cat.id,
        'name': cat.name,
        'subcategories': [{
            'id': sub.id,
            'name': sub.name
        } for sub in cat.subcategories.all()]
    } for cat in categories]

    return JsonResponse(categories_data, safe=False)


@login_required
@require_http_methods(["POST"])
def customer_report_submit(request):
    """API endpoint for submitting customer repair report"""
    if not is_customer(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        customer = Customer.objects.get(user=request.user)
        data = json.loads(request.body)

        from .models import Bike, RepairSubCategory

        # Validate bike belongs to customer
        bike_id = data.get('bike')
        try:
            bike = Bike.objects.get(id=bike_id, customer=customer)
        except Bike.DoesNotExist:
            return JsonResponse({'error': 'Bike not found or does not belong to you'}, status=400)

        # Create repair job
        repair = RepairJob.objects.create(
            bike=bike,
            problem_description=data.get('problem_description', ''),
            status='reported'
        )

        # Add subcategories if provided
        subcategory_ids = data.get('subcategories', [])
        if subcategory_ids:
            subcategories = RepairSubCategory.objects.filter(id__in=subcategory_ids)
            repair.subcategories.set(subcategories)

        return JsonResponse({
            'success': True,
            'repair_id': repair.id,
            'message': 'הדיווח נשלח בהצלחה!'
        })

    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
def repair_form_submit(request):
    """API endpoint for creating a new repair job"""
    try:
        from .models import RepairJob, Bike, RepairSubCategory
        from .helpers import is_manager
        import json

        data = json.loads(request.body)

        # Validate required fields
        bike_id = data.get('bike_id')
        if not bike_id:
            return JsonResponse({'error': 'Bike ID is required'}, status=400)

        # Get bike
        try:
            bike = Bike.objects.get(id=bike_id)
        except Bike.DoesNotExist:
            return JsonResponse({'error': 'Bike not found'}, status=404)

        # Create repair job
        repair = RepairJob.objects.create(
            bike=bike,
            problem_description=data.get('problem_description', ''),
            diagnosis=data.get('diagnosis', ''),
            status='reported'
        )

        # Add subcategories
        subcategory_ids = data.get('subcategory_ids', [])
        if subcategory_ids:
            subcategories = RepairSubCategory.objects.filter(id__in=subcategory_ids)
            repair.subcategories.set(subcategories)

        # If manager entered diagnosis, redirect to diagnosis page
        redirect_to_diagnosis = is_manager(request.user) and repair.diagnosis

        return JsonResponse({
            'success': True,
            'repair_id': repair.id,
            'redirect_to_diagnosis': redirect_to_diagnosis,
            'message': 'התיקון נוצר בהצלחה!'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)