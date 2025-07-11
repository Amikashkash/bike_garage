#!/usr/bin/env python
"""
יצירת משתמשי דמו עם groups נכונים
"""
import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User, Group

def create_demo_users():
    """יצירת משתמשי דמו עם Groups"""
    
    # יצירת Groups אם לא קיימים
    mechanic_group, created = Group.objects.get_or_create(name='Mechanic')
    if created:
        print("✅ נוצר Group: Mechanic")
    
    manager_group, created = Group.objects.get_or_create(name='Manager')
    if created:
        print("✅ נוצר Group: Manager")
    
    # יצירת מכונאי
    mechanic_user, created = User.objects.get_or_create(
        username='mechanic',
        defaults={
            'first_name': 'מכונאי',
            'last_name': 'דמו',
            'email': 'mechanic@demo.com'
        }
    )
    
    if created:
        mechanic_user.set_password('1234')
        mechanic_user.save()
        print("✅ נוצר משתמש מכונאי: mechanic")
    else:
        print("ℹ️ משתמש מכונאי כבר קיים")
    
    # הוספה לקבוצה
    if not mechanic_user.groups.filter(name='Mechanic').exists():
        mechanic_user.groups.add(mechanic_group)
        print("✅ מכונאי הוסף לקבוצת Mechanic")
    
    # יצירת מנהל
    manager_user, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'first_name': 'מנהל',
            'last_name': 'דמו',
            'email': 'manager@demo.com'
        }
    )
    
    if created:
        manager_user.set_password('1234')
        manager_user.save()
        print("✅ נוצר משתמש מנהל: manager")
    else:
        print("ℹ️ משתמש מנהל כבר קיים")
    
    # הוספה לקבוצה
    if not manager_user.groups.filter(name='Manager').exists():
        manager_user.groups.add(manager_group)
        print("✅ מנהל הוסף לקבוצת Manager")
    
    print("\n🎉 משתמשי דמו מוכנים:")
    print("👨‍🔧 מכונאי: mechanic / 1234")
    print("👨‍💼 מנהל: manager / 1234")

if __name__ == '__main__':
    print("=" * 50)
    print("🚴‍♂️ יצירת משתמשי דמו")
    print("=" * 50)
    
    try:
        create_demo_users()
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        print("💡 ודא שהרצת migrations: python manage.py migrate")
