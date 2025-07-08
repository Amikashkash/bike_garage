from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workshop.models import UserProfile

class Command(BaseCommand):
    help = 'ניקוי UserProfile כפולים'

    def handle(self, *args, **options):
        # מוצא משתמשים ללא UserProfile
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        for user in users_without_profile:
            # בדיקה אם המשתמש הוא superuser
            if user.is_superuser:
                UserProfile.objects.create(user=user, role='manager')
                self.stdout.write(f'נוצר פרופיל מנהל עבור: {user.username}')
            else:
                UserProfile.objects.create(user=user, role='customer')
                self.stdout.write(f'נוצר פרופיל לקוח עבור: {user.username}')

        # מוצא ומסיר UserProfile כפולים
        duplicate_profiles = []
        seen_users = set()
        
        for profile in UserProfile.objects.all():
            if profile.user_id in seen_users:
                duplicate_profiles.append(profile)
            else:
                seen_users.add(profile.user_id)
        
        if duplicate_profiles:
            for profile in duplicate_profiles:
                self.stdout.write(f'מוחק פרופיל כפול עבור: {profile.user.username}')
                profile.delete()
        
        self.stdout.write(self.style.SUCCESS('ניקוי הושלם בהצלחה!'))
