#!/usr/bin/env python3
"""
יצירת טכנאי חדש - דרך מהירה
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

def create_simple_technician(username):
    """יצירת טכנאי בדרך פשוטה"""
    
    print(f"🔧 יוצר טכנאי: {username}")
    
    # בדיקה אם קיים
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"❌ משתמש {username} כבר קיים!")
        
        # אולי יש לו פרופיל?
        try:
            profile = user.userprofile
            if profile.role == 'mechanic':
                print(f"✅ {username} כבר טכנאי")
            else:
                profile.role = 'mechanic'
                profile.save()
                print(f"✅ שונה תפקיד של {username} ל-mechanic")
        except:
            print(f"⚠️ אין פרופיל ל-{username}, יוצר...")
            try:
                UserProfile.objects.create(user=user, role='mechanic')
                print(f"✅ נוצר פרופיל mechanic ל-{username}")
            except Exception as e:
                print(f"❌ שגיאה: {e}")
        return
    
    # יצירת משתמש חדש
    try:
        user = User.objects.create_user(
            username=username,
            password='test123',
            first_name='טכנאי',
            last_name=username,
            email=f'{username}@test.com'
        )
        print(f"✅ נוצר משתמש: {username}")
        
        # יצירת פרופיל
        profile = UserProfile.objects.create(
            user=user,
            role='mechanic'
        )
        print(f"✅ נוצר פרופיל mechanic")
        print(f"🔑 סיסמה: test123")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        create_simple_technician(username)
    else:
        username = input("שם משתמש לטכנאי: ")
        create_simple_technician(username)
