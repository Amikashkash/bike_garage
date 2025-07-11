#!/usr/bin/env python
"""
סקריפט לבדיקת שגיאות אפשריות במערכת לפני deployment
"""

import os
import django
import sys

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def check_imports():
    """בדיקת כל ה-imports הנדרשים"""
    print("🔍 בדיקת imports...")
    
    try:
        from django.conf import settings
        from django.core.management import execute_from_command_line
        print("✅ Django imports - OK")
    except ImportError as e:
        print(f"❌ Django import error: {e}")
        return False
    
    try:
        from workshop.models import Customer, Bike, RepairJob, UserProfile
        print("✅ Workshop models - OK")
    except ImportError as e:
        print(f"❌ Workshop models import error: {e}")
        return False
    
    try:
        from workshop.views import home, register, user_logout
        print("✅ Workshop views - OK")
    except ImportError as e:
        print(f"❌ Workshop views import error: {e}")
        return False
    
    try:
        from workshop.forms import CustomerRegisterForm, BikeForm
        print("✅ Workshop forms - OK")
    except ImportError as e:
        print(f"❌ Workshop forms import error: {e}")
        return False
    
    return True

def check_database():
    """בדיקת התחברות למסד נתונים"""
    print("\n🔍 בדיקת מסד נתונים...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Database connection - OK")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def check_migrations():
    """בדיקת מצב migrations"""
    print("\n🔍 בדיקת migrations...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # בדיקת migrations שטרם הורצו
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        output = out.getvalue()
        
        if '[ ]' in output:
            print("⚠️  יש migrations שטרם הורצו")
            print("להרצה: python manage.py migrate")
        else:
            print("✅ כל המigrations הורצו")
        
        return True
    except Exception as e:
        print(f"❌ Migrations check error: {e}")
        return False

def check_static_files():
    """בדיקת קבצים סטטיים"""
    print("\n🔍 בדיקת קבצים סטטיים...")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.storage import staticfiles_storage
        
        print(f"STATIC_URL: {settings.STATIC_URL}")
        print(f"STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}")
        print(f"STATICFILES_DIRS: {getattr(settings, 'STATICFILES_DIRS', 'Not set')}")
        
        # בדיקה אם תיקיית static קיימת
        if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
            for static_dir in settings.STATICFILES_DIRS:
                if os.path.exists(static_dir):
                    print(f"✅ Static directory exists: {static_dir}")
                else:
                    print(f"⚠️  Static directory missing: {static_dir}")
        
        return True
    except Exception as e:
        print(f"❌ Static files check error: {e}")
        return False

def check_templates():
    """בדיקת templates"""
    print("\n🔍 בדיקת templates...")
    
    try:
        from django.template.loader import get_template
        
        # בדיקת templates עיקריים
        templates_to_check = [
            'workshop/home.html',
            'workshop/register.html',
            'workshop/base.html'
        ]
        
        for template_name in templates_to_check:
            try:
                template = get_template(template_name)
                print(f"✅ Template found: {template_name}")
            except Exception as e:
                print(f"❌ Template missing: {template_name} - {e}")
        
        return True
    except Exception as e:
        print(f"❌ Templates check error: {e}")
        return False

def check_basic_functionality():
    """בדיקת פונקציונליות בסיסית"""
    print("\n🔍 בדיקת פונקציונליות בסיסית...")
    
    try:
        from django.contrib.auth.models import User
        from workshop.models import UserProfile
        
        # ספירת משתמשים
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        
        print(f"✅ Users in system: {user_count}")
        print(f"✅ User profiles: {profile_count}")
        
        # בדיקת superuser
        superuser_exists = User.objects.filter(is_superuser=True).exists()
        if superuser_exists:
            print("✅ Superuser exists")
        else:
            print("⚠️  No superuser found - create one with: python manage.py createsuperuser")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality check error: {e}")
        return False

def main():
    print("🚀 בדיקת מערכת לפני deployment".encode('utf-8', errors='ignore').decode('utf-8'))
    print("=" * 50)
    
    checks = [
        check_imports,
        check_database,
        check_migrations,
        check_static_files,
        check_templates,
        check_basic_functionality
    ]
    
    all_passed = True
    for check in checks:
        try:
            result = check()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Check failed with exception: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ כל הבדיקות עברו בהצלחה!")
        print("המערכת מוכנה לdeployment")
    else:
        print("❌ יש בעיות שיש לתקן לפני deployment")
    
    return all_passed

if __name__ == "__main__":
    main()
