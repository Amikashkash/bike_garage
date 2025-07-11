#!/usr/bin/env python
"""
יצירת נתוני דמו עבור הסביבה החדשה
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User, Group
from workshop.models import Customer, Bike, RepairJob

def create_all_demo_data():
    print("🚀 יוצר נתוני דמו...")
    
    # יצירת Groups
    mechanic_group, _ = Group.objects.get_or_create(name='Mechanic')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    print("✅ Groups נוצרו")
    
    # יצירת Admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@demo.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print("✅ Admin נוצר: admin / admin123")
    
    # יצירת משתמשי דמו
    mechanic, created = User.objects.get_or_create(
        username='mechanic',
        defaults={'email': 'mechanic@demo.com'}
    )
    if created:
        mechanic.set_password('1234')
        mechanic.save()
        mechanic.groups.add(mechanic_group)
        print("✅ מכונאי נוצר: mechanic / 1234")
    
    manager, created = User.objects.get_or_create(
        username='manager',
        defaults={'email': 'manager@demo.com'}
    )
    if created:
        manager.set_password('1234')
        manager.save()
        manager.groups.add(manager_group)
        print("✅ מנהל נוצר: manager / 1234")
    
    print("🎉 הכל מוכן!")
    print("🌐 Admin: https://your-app.onrender.com/admin/")
    print("👤 משתמשים: mechanic/1234, manager/1234")

if __name__ == '__main__':
    create_all_demo_data()
