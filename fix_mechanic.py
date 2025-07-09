#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

user = User.objects.get(username='mechanic_test')
profile = user.userprofile
profile.role = 'mechanic'
profile.save()
print(f'תיקון תפקיד עבור {user.username}: {profile.role}')
