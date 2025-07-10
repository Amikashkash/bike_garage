#!/usr/bin/env python3
"""
מציג פרטי התחברות למשתמשי הדמו
"""

import os
import sys
import django

# הגדרת נתיב Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

def show_demo_users():
    """מציג רשימת משתמשים לדמו"""
    
    print("👥 משתמשי דמו למערכת:")
    print("=" * 50)
    
    # מציאת כל המשתמשים עם פרופילים
    for user in User.objects.filter(userprofile__isnull=False):
        profile = user.userprofile
        print(f"\n🔑 שם משתמש: {user.username}")
        print(f"📝 שם מלא: {user.get_full_name() or 'לא צוין'}")
        print(f"👤 תפקיד: {profile.get_role_display()}")
        print(f"📧 אימייל: {user.email or 'לא צוין'}")
        
        if user.username.endswith('_demo'):
            print(f"🔐 סיסמה: demo123")
        else:
            print(f"🔐 סיסמה: ניתן לנסות 'admin123' או 'demo123'")
    
    print("\n" + "=" * 50)
    print("🌐 כתובת התחברות: http://127.0.0.1:8000/accounts/login/")
    print("🏠 דף הבית: http://127.0.0.1:8000/")
    
    # מציאת תיקונים פעילים
    from workshop.models import RepairJob
    active_repairs = RepairJob.objects.filter(status__in=['in_progress', 'approved', 'partially_approved'])
    
    if active_repairs:
        print(f"\n🔧 תיקונים פעילים ({active_repairs.count()}):")
        for repair in active_repairs:
            print(f"   • תיקון #{repair.id} - {repair.bike} - {repair.get_status_display()}")
            if repair.assigned_mechanic:
                print(f"     מכונאי: {repair.assigned_mechanic.get_full_name()}")
            print(f"     צפייה: http://127.0.0.1:8000/workshop/repair/{repair.id}/status/")

if __name__ == '__main__':
    show_demo_users()
