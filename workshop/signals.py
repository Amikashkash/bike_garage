from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

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
