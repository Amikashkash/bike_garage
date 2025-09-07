"""
Push Notification Service for Bike Garage
Handles sending push notifications to customers using Web Push API
"""

import json
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.utils import timezone
from pywebpush import webpush, WebPushException
from .models import PushSubscription, CustomerNotification, Customer


logger = logging.getLogger(__name__)


class PushNotificationService:
    """Service for sending push notifications to customers"""
    
    def __init__(self):
        # VAPID keys for push notifications
        # In production, these should be in environment variables
        self.vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', None)
        self.vapid_public_key = getattr(settings, 'VAPID_PUBLIC_KEY', None)
        self.vapid_claims = {
            "sub": getattr(settings, 'VAPID_CLAIM_EMAIL', 'mailto:admin@bikegarage.com')
        }
        
        if not self.vapid_private_key or not self.vapid_public_key:
            logger.warning("VAPID keys not configured. Push notifications will not work.")
    
    def send_notification_to_customer(
        self, 
        customer: Customer, 
        title: str, 
        message: str, 
        notification_type: str = 'repair_update',
        action_url: str = '',
        icon: str = '/static/images/logo.png'
    ) -> bool:
        """
        Send push notification to all active subscriptions of a customer
        
        Args:
            customer: Customer to send to
            title: Notification title
            message: Notification body
            notification_type: Type from CustomerNotification.NOTIFICATION_TYPES
            action_url: URL to open when clicked
            icon: Icon URL
            
        Returns:
            True if at least one notification was sent successfully
        """
        if not self.vapid_private_key:
            logger.error("Cannot send push notification: VAPID keys not configured")
            return False
        
        # Get all active push subscriptions for this customer
        subscriptions = PushSubscription.objects.filter(
            customer=customer,
            is_active=True
        )
        
        if not subscriptions.exists():
            logger.info(f"No active push subscriptions found for customer {customer.id}")
            return False
        
        # Prepare notification data
        notification_data = {
            'title': title,
            'body': message,
            'icon': icon,
            'badge': '/static/images/logo.png',
            'data': {
                'action_url': action_url,
                'notification_type': notification_type,
                'customer_id': customer.id,
                'timestamp': timezone.now().isoformat()
            },
            'actions': [
                {
                    'action': 'view',
                    'title': 'צפה בפרטים'
                },
                {
                    'action': 'dismiss',
                    'title': 'ביטול'
                }
            ],
            'requireInteraction': notification_type in ['approval_needed', 'ready_for_pickup'],
            'vibrate': [200, 100, 200] if notification_type == 'ready_for_pickup' else [100]
        }
        
        # Special styling for different notification types
        if notification_type == 'approval_needed':
            notification_data['badge'] = '/static/pwa-icon.svg'
            notification_data['tag'] = 'approval-needed'
            notification_data['renotify'] = True
            
        elif notification_type == 'ready_for_pickup':
            notification_data['badge'] = '/static/pwa-icon.svg'
            notification_data['tag'] = 'ready-for-pickup'
            notification_data['renotify'] = True
            notification_data['vibrate'] = [300, 100, 300, 100, 300]
        
        success_count = 0
        
        # Send to each subscription
        for subscription in subscriptions:
            try:
                self._send_to_subscription(subscription, notification_data)
                subscription.mark_success()
                success_count += 1
                
            except Exception as e:
                logger.error(f"Failed to send push notification to subscription {subscription.id}: {e}")
                subscription.mark_failure()
        
        logger.info(f"Push notification sent to {success_count}/{len(subscriptions)} subscriptions for customer {customer.id}")
        return success_count > 0
    
    def _send_to_subscription(self, subscription: PushSubscription, notification_data: Dict[str, Any]):
        """Send push notification to a specific subscription"""
        
        try:
            response = webpush(
                subscription_info=subscription.subscription_info,
                data=json.dumps(notification_data),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims
            )
            
            logger.debug(f"Push notification sent successfully to {subscription.id}: {response.status_code}")
            
        except WebPushException as e:
            if e.response and e.response.status_code == 410:
                # Subscription expired/invalid
                logger.info(f"Push subscription {subscription.id} expired, marking as inactive")
                subscription.is_active = False
                subscription.save()
            raise e
    
    def send_approval_needed_notification(self, customer: Customer, repair_job, items_count: int):
        """Send notification when customer approval is needed"""
        title = "נדרש אישור ללקוח"
        message = f"יש {items_count} פריטים הממתינים לאישור עבור תיקון #{repair_job.id}"
        action_url = f"/repair/{repair_job.id}/approve/"
        
        return self.send_notification_to_customer(
            customer=customer,
            title=title,
            message=message,
            notification_type='approval_needed',
            action_url=action_url
        )
    
    def send_ready_for_pickup_notification(self, customer: Customer, repair_job):
        """Send notification when bike is ready for pickup"""
        bike_info = f"{repair_job.bike.brand} {repair_job.bike.model or ''}".strip()
        title = "🎉 האופניים מוכנים לאיסוף!"
        message = f"{bike_info} - התיקון הושלם בהצלחה. ניתן לאסוף מהמוסך."
        action_url = f"/customer/repairs/"
        
        return self.send_notification_to_customer(
            customer=customer,
            title=title,
            message=message,
            notification_type='ready_for_pickup',
            action_url=action_url
        )
    
    def send_repair_update_notification(self, customer: Customer, repair_job, status_display: str):
        """Send notification for general repair updates"""
        bike_info = f"{repair_job.bike.brand} {repair_job.bike.model or ''}".strip()
        title = "עדכון תיקון"
        message = f"{bike_info} - הסטטוס עודכן ל: {status_display}"
        action_url = f"/repair/{repair_job.id}/status/"
        
        return self.send_notification_to_customer(
            customer=customer,
            title=title,
            message=message,
            notification_type='repair_update',
            action_url=action_url
        )
    
    def create_and_send_notification(
        self,
        customer: Customer,
        repair_job,
        notification_type: str,
        title: str,
        message: str,
        action_url: str = ''
    ):
        """Create database notification and send push notification"""
        
        # Create database notification
        notification = CustomerNotification.objects.create(
            customer=customer,
            repair_job=repair_job,
            notification_type=notification_type,
            title=title,
            message=message,
            action_url=action_url
        )
        
        # Send push notification
        push_sent = self.send_notification_to_customer(
            customer=customer,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url
        )
        
        # Update notification with push status
        if push_sent:
            notification.is_push_sent = True
            notification.push_sent_at = timezone.now()
            notification.save()
        
        return notification, push_sent


# Global instance
push_service = PushNotificationService()