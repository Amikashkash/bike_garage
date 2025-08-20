"""
API views for handling push notifications and customer notifications
"""
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from .models import Customer, CustomerNotification
from .notification_service import NotificationService

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def register_push_subscription(request):
    """Register a push notification subscription for a customer"""
    try:
        data = json.loads(request.body)
        
        # Get customer from session or request
        customer_id = data.get('customer_id') or request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'Customer not identified'})
        
        customer = get_object_or_404(Customer, id=customer_id)
        
        subscription_data = {
            'endpoint': data.get('endpoint'),
            'keys': data.get('keys', {}),
            'userAgent': request.META.get('HTTP_USER_AGENT', ''),
            'deviceType': data.get('deviceType', 'unknown')
        }
        
        subscription = NotificationService.register_push_subscription(customer, subscription_data)
        
        return JsonResponse({
            'success': True,
            'message': 'התראות דחיפה הופעלו בהצלחה',
            'subscription_id': subscription.id
        })
        
    except Exception as e:
        logger.error(f"Error registering push subscription: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def unregister_push_subscription(request):
    """Unregister a push notification subscription"""
    try:
        data = json.loads(request.body)
        
        customer_id = data.get('customer_id') or request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'Customer not identified'})
        
        customer = get_object_or_404(Customer, id=customer_id)
        endpoint = data.get('endpoint')
        
        success = NotificationService.unregister_push_subscription(customer, endpoint)
        
        return JsonResponse({
            'success': success,
            'message': 'התראות דחיפה הופסקו' if success else 'שגיאה בהפסקת התראות'
        })
        
    except Exception as e:
        logger.error(f"Error unregistering push subscription: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@require_http_methods(["GET"])
def get_vapid_public_key(request):
    """Return the VAPID public key for push notifications"""
    from django.conf import settings
    return JsonResponse({
        'publicKey': getattr(settings, 'VAPID_PUBLIC_KEY', '')
    })


@require_http_methods(["GET"])
def get_notifications(request):
    """Get notifications for a customer"""
    try:
        customer_id = request.GET.get('customer_id') or request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'Customer not identified'})
        
        customer = get_object_or_404(Customer, id=customer_id)
        
        # Get paginated notifications
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        offset = (page - 1) * limit
        
        notifications = customer.notifications.all()[offset:offset + limit]
        unread_count = NotificationService.get_unread_notifications(customer)
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'type': notification.notification_type,
                'title': notification.title,
                'message': notification.message,
                'action_url': notification.action_url,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat(),
                'repair_id': notification.repair_job.id if notification.repair_job else None
            })
        
        return JsonResponse({
            'success': True,
            'notifications': notifications_data,
            'unread_count': unread_count,
            'has_more': len(notifications) == limit
        })
        
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def mark_notification_read(request):
    """Mark a notification as read"""
    try:
        data = json.loads(request.body)
        
        customer_id = data.get('customer_id') or request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'Customer not identified'})
        
        customer = get_object_or_404(Customer, id=customer_id)
        notification_id = data.get('notification_id')
        
        success = NotificationService.mark_notification_as_read(notification_id, customer)
        
        return JsonResponse({
            'success': success,
            'message': 'ההתראה סומנה כנקראה' if success else 'שגיאה בסימון ההתראה'
        })
        
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read for a customer"""
    try:
        data = json.loads(request.body)
        
        customer_id = data.get('customer_id') or request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'Customer not identified'})
        
        customer = get_object_or_404(Customer, id=customer_id)
        
        count = NotificationService.mark_all_notifications_as_read(customer)
        
        return JsonResponse({
            'success': True,
            'message': f'{count} התראות סומנו כנקראות',
            'marked_count': count
        })
        
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def test_notification(request):
    """Send a test notification (for development only)"""
    try:
        data = json.loads(request.body)
        
        customer_id = data.get('customer_id') or request.session.get('customer_id')
        if not customer_id:
            return JsonResponse({'success': False, 'error': 'Customer not identified'})
        
        customer = get_object_or_404(Customer, id=customer_id)
        
        notification = NotificationService.create_notification(
            customer=customer,
            notification_type='repair_update',
            title='הודעת בדיקה 🔧',
            message='זוהי הודעת בדיקה לוודא שההתראות פועלות כראוי.',
            action_url='/',
            send_push=True,
            send_email=False
        )
        
        return JsonResponse({
            'success': True,
            'message': 'הודעת בדיקה נשלחה בהצלחה',
            'notification_id': notification.id
        })
        
    except Exception as e:
        logger.error(f"Error sending test notification: {e}")
        return JsonResponse({'success': False, 'error': str(e)})
