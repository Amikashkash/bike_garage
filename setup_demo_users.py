#!/usr/bin/env python3
"""
יצירת נתוני בדיקה ומשתמש מנהל - ENDURO BIKE GARAGE
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
from workshop.models import UserProfile, Customer, Bike, RepairJob, RepairItem

def main():
    print("🚵‍♂️ ENDURO BIKE GARAGE - יצירת נתוני בדיקה")
    print("=" * 60)
    
    # יצירת משתמש מנהל
    try:
        manager_user = User.objects.get(username="manager")
        print("✅ משתמש מנהל כבר קיים")
    except User.DoesNotExist:
        manager_user = User.objects.create_user(
            username="manager",
            password="manager123",
            email="manager@endurobikegarage.com",
            first_name="מנהל",
            last_name="המוסך",
            is_staff=True,
            is_superuser=True
        )
        print("✅ נוצר משתמש מנהל חדש")
    
    # יצירת/עדכון פרופיל מנהל
    profile, created = UserProfile.objects.get_or_create(
        user=manager_user,
        defaults={'role': 'manager'}
    )
    if profile.role != 'manager':
        profile.role = 'manager'
        profile.save()
    print(f"✅ פרופיל מנהל {'נוצר' if created else 'עודכן'}")
    
    # יצירת משתמש טכנאי
    try:
        mechanic_user = User.objects.get(username="mechanic")
        print("✅ משתמש טכנאי כבר קיים")
    except User.DoesNotExist:
        mechanic_user = User.objects.create_user(
            username="mechanic",
            password="mechanic123",
            email="mechanic@endurobikegarage.com",
            first_name="עמית",
            last_name="הטכנאי"
        )
        print("✅ נוצר משתמש טכנאי חדש")
    
    profile, created = UserProfile.objects.get_or_create(
        user=mechanic_user,
        defaults={'role': 'mechanic'}
    )
    if profile.role != 'mechanic':
        profile.role = 'mechanic'
        profile.save()
    
    print("\n🔑 פרטי התחברות:")
    print(f"מנהל - שם משתמש: manager, סיסמה: manager123")
    print(f"טכנאי - שם משתמש: mechanic, סיסמה: mechanic123")
    
    print("\n📍 נתיבים חשובים:")
    print("🏠 דף הבית: http://127.0.0.1:8000/")
    print("🔐 התחברות: http://127.0.0.1:8000/login/")
    print("📊 דשבורד מנהל: http://127.0.0.1:8000/manager/dashboard/")
    print("🔧 משימות טכנאי: http://127.0.0.1:8000/mechanic/task/")
    print("⚙️ ניהול Django: http://127.0.0.1:8000/admin/")
    
    print(f"\n🎯 כעת ניתן להתחבר ולגשת לדשבורד המנהל!")
    print("🚀 המערכת מוכנה לפעולה עם העיצוב האקסטרימי החדש!")

if __name__ == "__main__":
    main()
