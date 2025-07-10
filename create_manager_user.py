#!/usr/bin/env python3
"""
יצירת משתמש מנהל למערכת ENDURO BIKE GARAGE
"""

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

def create_manager_user():
    """יצירת משתמש מנהל"""
    
    print("🚵‍♂️ ENDURO BIKE GARAGE - יצירת משתמש מנהל")
    print("=" * 50)
    
    username = "manager"
    password = "manager123"
    email = "manager@endurobikegarage.com"
    
    # בדיקה אם המשתמש כבר קיים
    if User.objects.filter(username=username).exists():
        print(f"✅ משתמש מנהל '{username}' כבר קיים")
        user = User.objects.get(username=username)
    else:
        # יצירת משתמש חדש
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name="מנהל",
            last_name="המוסך",
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ נוצר משתמש מנהל חדש: {username}")
    
    # בדיקה אם יש UserProfile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'manager'}
    )
    
    if created:
        print("✅ נוצר פרופיל מנהל חדש")
    else:
        if profile.role != 'manager':
            profile.role = 'manager'
            profile.save()
            print("✅ עודכן פרופיל למנהל")
        else:
            print("✅ פרופיל מנהל כבר קיים")
    
    print("\n🔑 פרטי התחברות:")
    print(f"שם משתמש: {username}")
    print(f"סיסמה: {password}")
    print(f"אימייל: {email}")
    
    print("\n🎯 כעת ניתן להתחבר כמנהל ולגשת לדשבורד!")
    print("📍 נתיב דשבורד: http://127.0.0.1:8000/manager/dashboard/")
    
    return user

def create_test_users():
    """יצירת משתמשי בדיקה נוספים"""
    
    print("\n🔧 יצירת משתמשי בדיקה נוספים...")
    
    # יצירת טכנאי
    if not User.objects.filter(username="mechanic").exists():
        mechanic_user = User.objects.create_user(
            username="mechanic",
            password="mechanic123",
            email="mechanic@endurobikegarage.com",
            first_name="עמית",
            last_name="הטכנאי"
        )
        UserProfile.objects.create(user=mechanic_user, role='mechanic')
        print("✅ נוצר משתמש טכנאי: mechanic")
    
    # יצירת לקוח
    if not User.objects.filter(username="customer").exists():
        customer_user = User.objects.create_user(
            username="customer",
            password="customer123",
            email="customer@endurobikegarage.com",
            first_name="יוסי",
            last_name="הלקוח"
        )
        UserProfile.objects.create(user=customer_user, role='customer')
        print("✅ נוצר משתמש לקוח: customer")

if __name__ == "__main__":
    create_manager_user()
    create_test_users()
    print("\n🏁 הושלם! המערכת מוכנה לפעולה! 🚵‍♂️")
