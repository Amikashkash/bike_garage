#!/usr/bin/env python3
"""
תיקון תפקיד המכונאי
"""

import os
import sys
import django

# הגדרת נתיב Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

def fix_mechanic_role():
    """תיקון תפקיד המכונאי"""
    
    user = User.objects.get(username='mechanic_demo')
    profile = UserProfile.objects.get(user=user)
    profile.role = 'mechanic'
    profile.save()
    print(f'✅ {user.username} עודכן להיות מכונאי')

if __name__ == '__main__':
    fix_mechanic_role()
