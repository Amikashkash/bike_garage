import os
import sys
import django
from pathlib import Path

# הוספת נתיב הפרויקט
project_path = Path(__file__).resolve().parent
sys.path.append(str(project_path))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

print("🔍 בדיקת מצב המערכת:")
print(f"משתמשים: {User.objects.count()}")
print(f"פרופילים: {UserProfile.objects.count()}")

# בדיקת משתמש מנהל
managers = User.objects.filter(userprofile__role='manager')
print(f"מנהלים: {managers.count()}")

if managers.exists():
    for manager in managers:
        print(f"  - {manager.username} ({manager.email})")

# יצירת משתמש מנהל אם לא קיים
if not managers.exists():
    print("🔧 יצירת משתמש מנהל...")
    
    user = User.objects.create_user(
        username='manager',
        password='manager123',
        email='manager@bikegarage.com',
        first_name='מנהל',
        last_name='המוסך',
        is_staff=True,
        is_superuser=True
    )
    
    profile = UserProfile.objects.create(
        user=user,
        role='manager'
    )
    
    print(f"✅ נוצר משתמש מנהל: {user.username}")
    print(f"✅ נוצר פרופיל: {profile.role}")

print("\n🎯 פרטי התחברות:")
print("שם משתמש: manager")
print("סיסמה: manager123")
print("\n📍 קישורים:")
print("🏠 http://127.0.0.1:8000/")
print("🔐 http://127.0.0.1:8000/login/")
print("📊 http://127.0.0.1:8000/manager/dashboard/")
print("🚀 http://127.0.0.1:8000/demo/dashboard/")
