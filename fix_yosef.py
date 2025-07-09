#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

user = User.objects.get(username='yosef_tech')
print(f'יש פרופיל: {hasattr(user, "userprofile")}')

if hasattr(user, 'userprofile'):
    print(f'תפקיד: {user.userprofile.role}')
    user.userprofile.role = 'mechanic'
    user.userprofile.save()
    print('תוקן לmechanic')
else:
    UserProfile.objects.create(user=user, role='mechanic')
    print('נוצר פרופיל mechanic חדש')
