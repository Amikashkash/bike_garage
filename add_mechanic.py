#!/usr/bin/env python3
"""
סקריפט ליצירת מכונאי לבדיקת זרימת העבודה המלאה
"""

import os
import sys
import django

# הגדרת Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

def create_mechanic():
    """יצירת מכונאי חדש לבדיקות"""
    
    # בדיקה אם המכונאי כבר קיים
    if User.objects.filter(username='mechanic_test').exists():
        print("המכונאי 'mechanic_test' כבר קיים!")
        user = User.objects.get(username='mechanic_test')
        
        # בדיקה אם יש לו פרופיל
        try:
            profile = user.userprofile
            print(f"פרטי המכונאי: {user.first_name} {user.last_name}, תפקיד: {profile.role}")
        except UserProfile.DoesNotExist:
            # יצירת פרופיל אם לא קיים
            profile = UserProfile.objects.create(
                user=user,
                role='mechanic'
            )
            print(f"נוצר פרופיל חדש עבור המכונאי: {user.username}")
            
        return user
    
    # יצירת משתמש חדש
    user = User.objects.create_user(
        username='mechanic_test',
        email='mechanic@bikegarage.test',
        password='test123',
        first_name='מכונאי',
        last_name='בדיקה'
    )
    
    # יצירת פרופיל מכונאי
    profile = UserProfile.objects.create(
        user=user,
        role='mechanic'
    )
    
    print(f"נוצר מכונאי חדש: {user.username}")
    print(f"שם מלא: {user.first_name} {user.last_name}")
    print(f"תפקיד: {profile.role}")
    print("סיסמה: test123")
    
    return user

if __name__ == '__main__':
    print("יוצר מכונאי לבדיקות...")
    create_mechanic()
    print("הושלם!")
