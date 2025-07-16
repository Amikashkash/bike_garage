import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from workshop.models import UserProfile

User = get_user_model()

# איפוס סיסמת המנהל
try:
    manager = User.objects.filter(userprofile__role='manager').first()
    if manager:
        print(f"מאפס סיסמה למנהל: {manager.username}")
        manager.set_password('test123')
        manager.save()
        print("✅ סיסמה אופסה")
    else:
        print("יוצר מנהל חדש...")
        manager = User.objects.create_user(
            username='manager_debug',
            password='test123',
            first_name='מנהל',
            last_name='דיבוג'
        )
        UserProfile.objects.create(user=manager, role='manager')
        print(f"✅ נוצר מנהל: {manager.username}")

except Exception as e:
    print(f"❌ שגיאה: {e}")
