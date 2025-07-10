import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

# Create manager user
user, created = User.objects.get_or_create(
    username='manager',
    defaults={
        'password': 'pbkdf2_sha256$600000$dummy$dummy',  # Will set below
        'email': 'manager@bikegarage.com',
        'first_name': 'מנהל',
        'last_name': 'המוסך',
        'is_staff': True,
        'is_superuser': True
    }
)

if created:
    user.set_password('manager123')
    user.save()

# Create profile
profile, created = UserProfile.objects.get_or_create(
    user=user,
    defaults={'role': 'manager'}
)

print(f"Manager user created/updated: {user.username}")
print(f"Profile created: {created}")
print("Login: manager / manager123")
