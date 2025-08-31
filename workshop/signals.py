from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, RepairJob, RepairItem, CustomerNotification
from .realtime_service import realtime_service

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # יצירת פרופיל רק אם לא קיים
        if not hasattr(instance, 'userprofile'):
            # בדיקה אם המשתמש הוא superuser
            role = 'manager' if instance.is_superuser else 'customer'
            UserProfile.objects.get_or_create(user=instance, defaults={'role': role})

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # שמירת פרופיל רק אם קיים
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


# Real-time notification signals
@receiver(post_save, sender=RepairJob)
def repair_job_status_changed(sender, instance, created, **kwargs):
    """Send real-time notifications when repair job status changes"""
    if created:
        # New repair job created - notify managers
        realtime_service.send_to_group(
            "managers",
            "new_repair_created",
            {
                'repair_id': instance.id,
                'customer_name': instance.bike.customer.name,
                'bike_info': f"{instance.bike.brand} {instance.bike.model}",
                'problem_description': instance.problem_description,
                'status': instance.status,  # Include status for counter updates
                'message': f"תיקון חדש נוצר: {instance.bike.brand} {instance.bike.model}"
            }
        )
        return
    
    # Check if status changed
    if hasattr(instance, '_original_status'):
        old_status = instance._original_status
        new_status = instance.status
        
        if old_status != new_status:
            # Status changed - send notifications
            realtime_service.repair_status_changed(instance, new_status)
            
            # Special notifications for specific status changes
            if new_status == 'awaiting_quality_check':
                realtime_service.quality_check_ready(instance)
            elif new_status == 'quality_approved':
                # Notify customer that repair is ready for pickup
                if instance.bike.customer.user:
                    realtime_service.send_to_group(
                        f"customer_{instance.bike.customer.user.id}",
                        "repair_ready_for_pickup",
                        {
                            'repair_id': instance.id,
                            'bike_info': f"{instance.bike.brand} {instance.bike.model}",
                            'message': f"תיקון מוכן לאיסוף: {instance.bike.brand} {instance.bike.model}"
                        }
                    )


@receiver(pre_save, sender=RepairJob)
def store_original_repair_status(sender, instance, **kwargs):
    """Store original status before saving to detect changes"""
    if instance.pk:
        try:
            original = RepairJob.objects.get(pk=instance.pk)
            instance._original_status = original.status
            instance._original_assigned_mechanic = original.assigned_mechanic
            instance._original_is_stuck = original.is_stuck
        except RepairJob.DoesNotExist:
            pass


@receiver(post_save, sender=RepairJob)
def mechanic_assignment_changed(sender, instance, created, **kwargs):
    """Handle mechanic assignment notifications"""
    if created:
        return
        
    # Check if mechanic assignment changed
    if hasattr(instance, '_original_assigned_mechanic'):
        old_mechanic = instance._original_assigned_mechanic
        new_mechanic = instance.assigned_mechanic
        
        if old_mechanic != new_mechanic and new_mechanic:
            # New mechanic assigned
            realtime_service.mechanic_assigned(instance, new_mechanic)


@receiver(post_save, sender=RepairJob)  
def stuck_status_changed(sender, instance, created, **kwargs):
    """Handle stuck repair notifications"""
    if created:
        return
        
    # Check if stuck status changed
    if hasattr(instance, '_original_is_stuck'):
        was_stuck = instance._original_is_stuck
        is_stuck = instance.is_stuck
        
        if not was_stuck and is_stuck:
            # Repair became stuck - notify managers
            realtime_service.mechanic_stuck(instance, instance.stuck_reason)
        elif was_stuck and not is_stuck and instance.stuck_resolved:
            # Repair no longer stuck - notify assigned mechanic
            if instance.assigned_mechanic:
                realtime_service.send_to_group(
                    f"mechanic_{instance.assigned_mechanic.id}",
                    "stuck_repair_resolved",
                    {
                        'repair_id': instance.id,
                        'bike_info': f"{instance.bike.brand} {instance.bike.model}",
                        'manager_response': instance.manager_response,
                        'message': f"תיקון שחרר: {instance.bike.brand} {instance.bike.model}"
                    }
                )


@receiver(post_save, sender=RepairItem)
def repair_item_status_changed(sender, instance, created, **kwargs):
    """Handle repair item status changes"""
    if created:
        return
        
    # Check if item was completed
    if hasattr(instance, '_original_status'):
        old_status = instance._original_status
        new_status = instance.status
        
        if old_status != 'completed' and new_status == 'completed':
            # Item completed - send progress update
            realtime_service.repair_item_completed(instance, instance.completed_by)


@receiver(pre_save, sender=RepairItem)
def store_original_item_status(sender, instance, **kwargs):
    """Store original status before saving to detect changes"""
    if instance.pk:
        try:
            original = RepairItem.objects.get(pk=instance.pk)
            instance._original_status = original.status
        except RepairItem.DoesNotExist:
            pass


@receiver(post_save, sender=CustomerNotification)
def customer_notification_created(sender, instance, created, **kwargs):
    """Send real-time notification when CustomerNotification is created"""
    if created:
        realtime_service.customer_notification_created(instance)


@receiver(post_save, sender=RepairJob)
def auto_update_customer_notifications(sender, instance, created, **kwargs):
    """Auto-create customer notifications for important status changes"""
    if created:
        return
        
    # Only proceed if status actually changed
    if not hasattr(instance, '_original_status'):
        return
        
    old_status = instance._original_status
    new_status = instance.status
    
    if old_status == new_status:
        return
    
    # Create customer notifications for important status changes
    notification_messages = {
        'diagnosed': {
            'title': 'אבחון התיקון הושלם',
            'message': f'אבחון התיקון של {instance.bike.brand} {instance.bike.model} הושלם. נדרש אישורך להמשך התיקון.',
            'type': 'approval_needed'
        },
        'approved': {
            'title': 'התיקון אושר',
            'message': f'התיקון של {instance.bike.brand} {instance.bike.model} אושר והועבר לביצוע.',
            'type': 'repair_update'
        },
        'quality_approved': {
            'title': 'התיקון מוכן לאיסוף',
            'message': f'התיקון של {instance.bike.brand} {instance.bike.model} הושלם ומוכן לאיסוף.',
            'type': 'ready_for_pickup'
        },
        'completed': {
            'title': 'התיקון הושלם',
            'message': f'התיקון של {instance.bike.brand} {instance.bike.model} הושלם בהצלחה.',
            'type': 'repair_update'
        }
    }
    
    if new_status in notification_messages:
        notification_data = notification_messages[new_status]
        
        # Create the notification
        CustomerNotification.objects.create(
            customer=instance.bike.customer,
            repair_job=instance,
            notification_type=notification_data['type'],
            title=notification_data['title'],
            message=notification_data['message'],
            action_url=f'/repair/{instance.id}/'
        )
