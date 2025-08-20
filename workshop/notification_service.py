"""
Notification service for sending push notifications and emails to customers
"""
import json
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from pywebpush import webpush, WebPushException
from .models import Customer, RepairJob, CustomerNotification, PushSubscription

logger = logging.getLogger(__name__)

# VAPID keys for push notifications (you should generate these and put in settings)
VAPID_PRIVATE_KEY = getattr(settings, 'VAPID_PRIVATE_KEY', None)
VAPID_PUBLIC_KEY = getattr(settings, 'VAPID_PUBLIC_KEY', "BK7vA-5jG9C3-7Xw9_5vY9_1Y8vJ2G8rZ3L4tE2hQ1mK5dR9_7Xw3V2N5cT8fE9kG2hL6dR7_4Xw1Y8vJ3L5tE9")
VAPID_CLAIMS = getattr(settings, 'VAPID_CLAIMS', {"sub": "mailto:admin@bike-garage.com"})


class NotificationService:
    """Service for managing customer notifications"""
    
    @staticmethod
    def create_notification(
        customer: Customer,
        notification_type: str,
        title: str,
        message: str,
        repair_job: Optional[RepairJob] = None,
        action_url: str = "",
        send_push: bool = True,
        send_email: bool = True
    ) -> CustomerNotification:
        """Create a new notification for a customer"""
        
        notification = CustomerNotification.objects.create(
            customer=customer,
            repair_job=repair_job,
            notification_type=notification_type,
            title=title,
            message=message,
            action_url=action_url
        )
        
        # Send push notification
        if send_push:
            NotificationService._send_push_notification(notification)
        
        # Send email notification
        if send_email and customer.email:
            NotificationService._send_email_notification(notification)
        
        return notification
    
    @staticmethod
    def notify_approval_needed(repair_job: RepairJob) -> CustomerNotification:
        """Notify customer that approval is needed for repair actions"""
        customer = repair_job.bike.customer
        title = f"נדרש אישור - תיקון {repair_job.bike}"
        message = f"האבחון לתיקון האופניים {repair_job.bike} מוכן. יש צורך באישור שלך לפעולות התיקון."
        
        action_url = reverse('customer_approval', kwargs={'repair_id': repair_job.id})
        
        return NotificationService.create_notification(
            customer=customer,
            notification_type='approval_needed',
            title=title,
            message=message,
            repair_job=repair_job,
            action_url=action_url
        )
    
    @staticmethod
    def notify_ready_for_pickup(repair_job: RepairJob) -> CustomerNotification:
        """Notify customer that bike is ready for pickup"""
        customer = repair_job.bike.customer
        title = f"האופניים מוכנים לאיסוף! 🚴‍♂️"
        message = f"התיקון של האופניים {repair_job.bike} הושלם בהצלחה ומוכן לאיסוף. אנא הגע למוסך לקחת את האופניים."
        
        action_url = reverse('repair_status', kwargs={'repair_id': repair_job.id})
        
        return NotificationService.create_notification(
            customer=customer,
            notification_type='ready_for_pickup',
            title=title,
            message=message,
            repair_job=repair_job,
            action_url=action_url
        )
    
    @staticmethod
    def notify_repair_update(repair_job: RepairJob, update_message: str) -> CustomerNotification:
        """Notify customer about repair progress update"""
        customer = repair_job.bike.customer
        title = f"עדכון תיקון - {repair_job.bike}"
        message = f"יש עדכון חדש על תיקון האופניים {repair_job.bike}: {update_message}"
        
        action_url = reverse('repair_status', kwargs={'repair_id': repair_job.id})
        
        return NotificationService.create_notification(
            customer=customer,
            notification_type='repair_update',
            title=title,
            message=message,
            repair_job=repair_job,
            action_url=action_url
        )
    
    @staticmethod
    def notify_new_diagnosis(repair_job: RepairJob) -> CustomerNotification:
        """Notify customer about new diagnosis"""
        customer = repair_job.bike.customer
        title = f"אבחון חדש - {repair_job.bike}"
        message = f"האבחון לתיקון האופניים {repair_job.bike} הושלם. אנא צפה בפרטים ובפעולות המוצעות."
        
        action_url = reverse('repair_status', kwargs={'repair_id': repair_job.id})
        
        return NotificationService.create_notification(
            customer=customer,
            notification_type='new_diagnosis',
            title=title,
            message=message,
            repair_job=repair_job,
            action_url=action_url
        )
    
    @staticmethod
    def _send_push_notification(notification: CustomerNotification) -> bool:
        """Send push notification to customer's registered devices"""
        try:
            if not VAPID_PRIVATE_KEY or VAPID_PRIVATE_KEY == "development_mode_no_push":
                logger.info("Push notifications disabled in development mode")
                return False
            
            customer = notification.customer
            
            # Validate customer has valid contact info
            if not customer.phone and not customer.email:
                logger.warning(f"Customer {customer.name} has no contact information")
                return False
            
            subscriptions = customer.push_subscriptions.filter(is_active=True)
            
            if not subscriptions.exists():
                logger.info(f"No active push subscriptions for customer {customer.name}")
                return False
            
            success_count = 0
            for subscription in subscriptions:
                try:
                    payload = {
                        "title": notification.title,
                        "body": notification.message,
                        "icon": "/static/images/logo.png",
                        "badge": "/static/images/logo.png",
                        "data": {
                            "notification_id": notification.id,
                            "action_url": notification.action_url,
                            "repair_id": notification.repair_job.id if notification.repair_job else None
                        },
                        "actions": [
                            {
                                "action": "view",
                                "title": "צפה בפרטים",
                                "icon": "/static/icons/view.png"
                            }
                        ],
                        "requireInteraction": notification.notification_type in ['approval_needed', 'ready_for_pickup'],
                        "vibrate": [200, 100, 200] if notification.notification_type == 'ready_for_pickup' else [100]
                    }
                    
                    webpush(
                        subscription_info={
                            "endpoint": subscription.endpoint,
                            "keys": {
                                "p256dh": subscription.p256dh_key,
                                "auth": subscription.auth_key
                            }
                        },
                        data=json.dumps(payload),
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims=VAPID_CLAIMS
                    )
                    
                    success_count += 1
                    logger.info(f"Push notification sent successfully to {customer.name}")
                    
                except WebPushException as e:
                    logger.error(f"Failed to send push notification to {customer.name}: {e}")
                    if e.response and e.response.status_code in [400, 404, 410]:
                        # Invalid subscription, deactivate it
                        subscription.is_active = False
                        subscription.save()
                except Exception as e:
                    logger.error(f"Unexpected error sending push notification: {e}")
            
            if success_count > 0:
                notification.is_push_sent = True
                notification.push_sent_at = timezone.now()
                notification.save()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Critical error in push notification service: {e}")
            return False
    
    @staticmethod
    def _send_email_notification(notification: CustomerNotification) -> bool:
        """Send email notification to customer"""
        try:
            customer = notification.customer
            
            # Skip if no email
            if not customer.email or '@' not in customer.email:
                logger.info(f"Customer {customer.name} has no valid email address")
                return False
            
            subject = f"מוסך האופניים - {notification.title}"
            
            # Create email body with action link
            base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
            action_link = f"{base_url}{notification.action_url}" if notification.action_url else base_url
            
            email_body = f"""
שלום {customer.name},

{notification.message}

אם ברצונך לצפות בפרטים נוספים, לחץ על הקישור הבא:
{action_link}

בברכה,
מוסך האופניים

---
הודעה זו נשלחה אוטומטית ממערכת ניהול מוסך האופניים.
"""
            
            send_mail(
                subject=subject,
                message=email_body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'garage@example.com'),
                recipient_list=[customer.email],
                fail_silently=False
            )
            
            notification.is_email_sent = True
            notification.email_sent_at = timezone.now()
            notification.save()
            
            logger.info(f"Email notification sent successfully to {customer.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification to {customer.email if hasattr(customer, 'email') else 'unknown'}: {e}")
            return False
    
    @staticmethod
    def register_push_subscription(customer: Customer, subscription_data: Dict[str, Any]) -> PushSubscription:
        """Register a new push subscription for a customer"""
        endpoint = subscription_data.get('endpoint')
        keys = subscription_data.get('keys', {})
        
        # Get or create subscription
        subscription, created = PushSubscription.objects.get_or_create(
            customer=customer,
            endpoint=endpoint,
            defaults={
                'p256dh_key': keys.get('p256dh', ''),
                'auth_key': keys.get('auth', ''),
                'user_agent': subscription_data.get('userAgent', ''),
                'device_type': subscription_data.get('deviceType', ''),
                'is_active': True
            }
        )
        
        if not created:
            # Update existing subscription
            subscription.p256dh_key = keys.get('p256dh', subscription.p256dh_key)
            subscription.auth_key = keys.get('auth', subscription.auth_key)
            subscription.is_active = True
            subscription.save()
        
        logger.info(f"Push subscription registered for {customer.name}")
        return subscription
    
    @staticmethod
    def unregister_push_subscription(customer: Customer, endpoint: str) -> bool:
        """Unregister a push subscription"""
        try:
            subscription = PushSubscription.objects.get(customer=customer, endpoint=endpoint)
            subscription.is_active = False
            subscription.save()
            logger.info(f"Push subscription unregistered for {customer.name}")
            return True
        except PushSubscription.DoesNotExist:
            logger.warning(f"Attempted to unregister non-existent subscription for {customer.name}")
            return False
    
    @staticmethod
    def get_unread_notifications(customer: Customer) -> int:
        """Get count of unread notifications for customer"""
        return customer.notifications.filter(is_read=False).count()
    
    @staticmethod
    def mark_notification_as_read(notification_id: int, customer: Customer) -> bool:
        """Mark a specific notification as read"""
        try:
            notification = customer.notifications.get(id=notification_id)
            notification.mark_as_read()
            return True
        except CustomerNotification.DoesNotExist:
            return False
    
    @staticmethod
    def mark_all_notifications_as_read(customer: Customer) -> int:
        """Mark all notifications as read for a customer"""
        unread_notifications = customer.notifications.filter(is_read=False)
        count = unread_notifications.count()
        
        for notification in unread_notifications:
            notification.mark_as_read()
        
        return count
