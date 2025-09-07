from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum
from django.utils import timezone
from .models import (
    Customer, RepairJob, CustomerNotification, RepairItem, 
    RepairCategory, RepairSubCategory
)
from .serializers import (
    RepairJobSerializer, CustomerNotificationSerializer, CustomerStatsSerializer,
    RepairCategorySerializer, RepairSubCategorySerializer
)


class IsCustomerPermission(permissions.BasePermission):
    """
    Custom permission to only allow customers to access their own data.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user has customer profile and get the customer object
        try:
            customer = Customer.objects.get(user=request.user)
            request.customer = customer
            return True
        except Customer.DoesNotExist:
            return False


@api_view(['GET'])
@permission_classes([IsCustomerPermission])
def customer_stats(request):
    """Get customer statistics for the home page"""
    customer = request.customer
    
    # Get all repair jobs for this customer
    repairs = RepairJob.objects.filter(bike__customer=customer)
    
    # Active repairs (not completed or delivered)
    active_repairs = repairs.exclude(status__in=['completed', 'delivered']).count()
    
    # Total repairs
    total_repairs = repairs.count()
    
    # Unread notifications
    unread_notifications = CustomerNotification.objects.filter(
        customer=customer,
        is_read=False
    ).count()
    
    # Ready for pickup - broader criteria to match frontend logic
    # Count repairs that are ready for pickup based on multiple criteria:
    # 1. Status is 'quality_approved' 
    # 2. Available_for_pickup field is True
    # 3. Status is 'approved' (since frontend displays this as ready for pickup)
    
    ready_for_pickup = repairs.filter(
        Q(status='quality_approved') |
        Q(available_for_pickup=True) |
        Q(status='approved')
    ).count()
    
    stats = {
        'active_repairs': active_repairs,
        'total_repairs': total_repairs,
        'notifications': unread_notifications,
        'ready_for_pickup': ready_for_pickup
    }
    
    serializer = CustomerStatsSerializer(stats)
    return Response(serializer.data)


class CustomerRepairListView(generics.ListAPIView):
    """List all repair jobs for the authenticated customer"""
    serializer_class = RepairJobSerializer
    permission_classes = [IsCustomerPermission]
    
    def get_queryset(self):
        customer = self.request.customer
        queryset = RepairJob.objects.filter(
            bike__customer=customer
        ).select_related(
            'bike', 'assigned_mechanic', 'quality_checked_by'
        ).prefetch_related(
            'subcategories__category', 'repair_items', 'updates'
        )
        
        # Add computed fields to the queryset
        return queryset.annotate(
            total_price=Sum('repair_items__price'),
            total_approved_price=Sum(
                'repair_items__price',
                filter=Q(repair_items__is_approved_by_customer=True)
            ),
            pending_approval_price=Sum(
                'repair_items__price',
                filter=Q(repair_items__is_approved_by_customer=False)
            ),
            completed_items_count=Count(
                'repair_items',
                filter=Q(repair_items__status='completed')
            ),
            approved_items_count=Count(
                'repair_items',
                filter=Q(repair_items__is_approved_by_customer=True)
            )
        )


class CustomerRepairDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific repair job"""
    serializer_class = RepairJobSerializer
    permission_classes = [IsCustomerPermission]
    
    def get_queryset(self):
        customer = self.request.customer
        return RepairJob.objects.filter(
            bike__customer=customer
        ).select_related(
            'bike', 'assigned_mechanic', 'quality_checked_by'
        ).prefetch_related(
            'subcategories__category', 'repair_items', 'updates'
        ).annotate(
            total_price=Sum('repair_items__price'),
            total_approved_price=Sum(
                'repair_items__price',
                filter=Q(repair_items__is_approved_by_customer=True)
            ),
            pending_approval_price=Sum(
                'repair_items__price',
                filter=Q(repair_items__is_approved_by_customer=False)
            ),
            completed_items_count=Count(
                'repair_items',
                filter=Q(repair_items__status='completed')
            ),
            approved_items_count=Count(
                'repair_items',
                filter=Q(repair_items__is_approved_by_customer=True)
            )
        )


@api_view(['POST'])
@permission_classes([IsCustomerPermission])
def approve_repair_items(request, repair_id):
    """Approve specific repair items"""
    customer = request.customer
    repair = get_object_or_404(RepairJob, id=repair_id, bike__customer=customer)
    
    item_ids = request.data.get('item_ids', [])
    if not item_ids:
        return Response(
            {'error': 'No items specified'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update the specified items
    updated_count = RepairItem.objects.filter(
        id__in=item_ids,
        repair_job=repair,
        is_approved_by_customer=False
    ).update(is_approved_by_customer=True)
    
    # Check if all items are now approved and update repair status
    if repair.repair_items.filter(is_approved_by_customer=False).count() == 0:
        repair.status = 'approved'
        repair.approved_at = timezone.now()
        repair.save()
    elif updated_count > 0:
        repair.status = 'partially_approved'
        repair.save()
    
    return Response({
        'message': f'{updated_count} items approved successfully',
        'repair_status': repair.get_status_display()
    })


class CustomerNotificationListView(generics.ListAPIView):
    """List all notifications for the authenticated customer"""
    serializer_class = CustomerNotificationSerializer
    permission_classes = [IsCustomerPermission]
    
    def get_queryset(self):
        customer = self.request.customer
        return CustomerNotification.objects.filter(
            customer=customer
        ).select_related('repair_job__bike').order_by('-created_at')


@api_view(['POST'])
@permission_classes([IsCustomerPermission])
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    customer = request.customer
    notification = get_object_or_404(
        CustomerNotification, 
        id=notification_id, 
        customer=customer
    )
    
    notification.mark_as_read()
    
    return Response({'message': 'Notification marked as read'})


@api_view(['POST'])
@permission_classes([IsCustomerPermission])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    customer = request.customer
    
    updated_count = CustomerNotification.objects.filter(
        customer=customer,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return Response({
        'message': f'{updated_count} notifications marked as read'
    })


class RepairCategoryListView(generics.ListAPIView):
    """List all repair categories (for creating new repairs)"""
    serializer_class = RepairCategorySerializer
    permission_classes = [IsCustomerPermission]
    queryset = RepairCategory.objects.all()


class RepairSubCategoryListView(generics.ListAPIView):
    """List subcategories for a specific category"""
    serializer_class = RepairSubCategorySerializer
    permission_classes = [IsCustomerPermission]
    
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return RepairSubCategory.objects.filter(category_id=category_id)
        return RepairSubCategory.objects.all()


@api_view(['GET'])
@permission_classes([IsCustomerPermission])
def active_repairs_summary(request):
    """Get a summary of active repairs with key information"""
    customer = request.customer
    
    active_repairs = RepairJob.objects.filter(
        bike__customer=customer
    ).exclude(
        status__in=['completed', 'delivered']
    ).select_related(
        'bike', 'assigned_mechanic'
    ).annotate(
        approved_items_count=Count(
            'repair_items',
            filter=Q(repair_items__is_approved_by_customer=True)
        ),
        completed_items_count=Count(
            'repair_items',
            filter=Q(repair_items__status='completed')
        )
    )
    
    summary_data = []
    for repair in active_repairs:
        summary_data.append({
            'id': repair.id,
            'bike_info': f"{repair.bike.brand} {repair.bike.model or ''}".strip(),
            'status': repair.get_status_display(),
            'status_code': repair.status,
            'created_at': repair.created_at,
            'progress_percentage': repair.get_progress_percentage(),
            'is_stuck': repair.is_effectively_stuck,
            'needs_approval': repair.repair_items.filter(
                is_approved_by_customer=False
            ).exists(),
            'ready_for_pickup': repair.status == 'quality_approved'
        })
    
    return Response(summary_data)