from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
import json


class RealtimeNotificationService:
    """Service for sending real-time notifications via WebSockets"""
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def send_to_group(self, group_name, event_type, data):
        """Send message to a WebSocket group"""
        if self.channel_layer:
            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    'type': event_type,
                    'timestamp': timezone.now().isoformat(),
                    **data
                }
            )
    
    def notify_customer(self, customer_user_id, notification_data):
        """Send notification to specific customer"""
        self.send_to_group(
            f"customer_{customer_user_id}",
            'customer_notification',
            notification_data
        )
    
    def notify_mechanic(self, mechanic_user_id, event_type, data):
        """Send notification to specific mechanic"""
        self.send_to_group(
            f"mechanic_{mechanic_user_id}",
            event_type,
            data
        )
    
    def notify_managers(self, event_type, data):
        """Send notification to all managers"""
        self.send_to_group(
            "managers",
            event_type,
            data
        )
    
    def notify_all_mechanics(self, event_type, data):
        """Send notification to all mechanics"""
        self.send_to_group(
            "mechanics",
            event_type,
            data
        )
    
    # Specific notification methods
    def repair_status_changed(self, repair_job, new_status, message=""):
        """Notify about repair status change"""
        # Notify customer
        if repair_job.bike.customer.user:
            self.notify_customer(
                repair_job.bike.customer.user.id,
                {
                    'repair_id': repair_job.id,
                    'status': new_status,
                    'status_display': repair_job.get_status_display(),
                    'bike_info': f"{repair_job.bike.brand} {repair_job.bike.model}",
                    'message': message or f"סטטוס התיקון שונה ל: {repair_job.get_status_display()}"
                }
            )
        
        # Notify assigned mechanic if exists
        if repair_job.assigned_mechanic:
            self.notify_mechanic(
                repair_job.assigned_mechanic.id,
                'repair_status_update',
                {
                    'repair_id': repair_job.id,
                    'status': new_status,
                    'message': message or f"סטטוס התיקון שונה ל: {repair_job.get_status_display()}"
                }
            )
    
    def mechanic_assigned(self, repair_job, mechanic_user):
        """Notify about mechanic assignment"""
        # Notify the assigned mechanic
        self.notify_mechanic(
            mechanic_user.id,
            'new_repair_assignment',
            {
                'repair_id': repair_job.id,
                'bike_info': f"{repair_job.bike.brand} {repair_job.bike.model}",
                'customer_name': repair_job.bike.customer.name,
                'problem_description': repair_job.problem_description,
                'message': f"הוקצה לך תיקון חדש: {repair_job.bike.brand} {repair_job.bike.model}"
            }
        )
        
        # Notify customer
        if repair_job.bike.customer.user:
            self.notify_customer(
                repair_job.bike.customer.user.id,
                {
                    'repair_id': repair_job.id,
                    'status': repair_job.status,
                    'mechanic_name': f"{mechanic_user.first_name} {mechanic_user.last_name}",
                    'message': f"הוקצה מכונאי לתיקון: {mechanic_user.first_name} {mechanic_user.last_name}"
                }
            )
    
    def mechanic_stuck(self, repair_job, reason):
        """Notify managers about stuck repair"""
        self.notify_managers(
            'mechanic_stuck_notification',
            {
                'repair_id': repair_job.id,
                'mechanic_name': f"{repair_job.assigned_mechanic.first_name} {repair_job.assigned_mechanic.last_name}" if repair_job.assigned_mechanic else "לא ידוע",
                'bike_info': f"{repair_job.bike.brand} {repair_job.bike.model}",
                'customer_name': repair_job.bike.customer.name,
                'reason': reason,
                'message': f"מכונאי תקוע בתיקון: {repair_job.bike.brand} {repair_job.bike.model}"
            }
        )
    
    def quality_check_ready(self, repair_job):
        """Notify managers about repair ready for quality check"""
        self.notify_managers(
            'quality_check_ready',
            {
                'repair_id': repair_job.id,
                'bike_info': f"{repair_job.bike.brand} {repair_job.bike.model}",
                'customer_name': repair_job.bike.customer.name,
                'mechanic_name': f"{repair_job.assigned_mechanic.first_name} {repair_job.assigned_mechanic.last_name}" if repair_job.assigned_mechanic else "לא ידוע",
                'message': f"תיקון מוכן לבדיקת איכות: {repair_job.bike.brand} {repair_job.bike.model}"
            }
        )
    
    def customer_notification_created(self, notification):
        """Notify customer about new notification"""
        if notification.customer.user:
            self.notify_customer(
                notification.customer.user.id,
                {
                    'notification_id': notification.id,
                    'title': notification.title,
                    'message': notification.message,
                    'notification_type': notification.notification_type,
                    'action_url': notification.action_url,
                    'repair_id': notification.repair_job.id if notification.repair_job else None
                }
            )
    
    def repair_item_completed(self, repair_item, completed_by_user):
        """Notify about repair item completion"""
        repair_job = repair_item.repair_job
        
        # Calculate progress
        total_approved = repair_job.get_approved_count()
        completed_count = repair_job.get_completed_count()
        progress = (completed_count / total_approved * 100) if total_approved > 0 else 0
        
        # Notify customer
        if repair_job.bike.customer.user:
            self.notify_customer(
                repair_job.bike.customer.user.id,
                {
                    'repair_id': repair_job.id,
                    'item_description': repair_item.description,
                    'progress': round(progress, 1),
                    'completed_count': completed_count,
                    'total_approved': total_approved,
                    'message': f"הושלמה פעולה: {repair_item.description}"
                }
            )
        
        # Notify managers if all items completed
        if progress >= 100:
            self.quality_check_ready(repair_job)


# Global instance
realtime_service = RealtimeNotificationService()