#!/usr/bin/env python
"""
בדיקת המערכת אחרי שגיאה
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def test_basic_imports():
    """בדיקת imports בסיסיים"""
    try:
        from django.contrib.auth.models import User
        print("✅ User model - OK")
        
        from workshop.models import Customer, Bike, RepairJob
        print("✅ Workshop models - OK")
        
        from workshop.forms import CustomerForm
        print("✅ Basic forms - OK")
        
        # בדיקת מסד נתונים
        user_count = User.objects.count()
        print(f"✅ Database connection - OK ({user_count} users)")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("🔍 בדיקת המערכת...")
    if test_basic_imports():
        print("✅ המערכת תקינה")
    else:
        print("❌ יש בעיות במערכת")
