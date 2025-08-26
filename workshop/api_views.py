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
    
    # Count stuck repairs
    stuck_repairs = RepairJob.objects.filter(is_stuck=True).count()
    
    # Count quality checks needed
    quality_checks = RepairJob.objects.filter(status='awaiting_quality_check').count()
    
    # Count new repairs (not yet assigned)
    new_repairs = RepairJob.objects.filter(
        status__in=['approved', 'partially_approved'],
        assigned_mechanic__isnull=True
    ).count()
    
    return JsonResponse({
        'stuck_repairs': stuck_repairs,
        'quality_checks': quality_checks,
        'new_repairs': new_repairs,
        'status': 'success'
    })


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