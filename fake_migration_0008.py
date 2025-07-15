#!/usr/bin/env python
"""
סימון מיגרציה 0008 כ-FAKED לאחר התיקון הידני
"""
import os
import django
from django.core.management import call_command

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def fake_migration():
    """סימון המיגרציה כ-FAKED"""
    print("🔧 מסמן מיגרציה 0008 כ-FAKED...")
    
    try:
        # סימון המיגרציה כ-FAKED
        call_command('migrate', 'workshop', '0008', '--fake')
        print("✅ מיגרציה 0008 סומנה כ-FAKED")
        
        # בדיקת מצב המיגרציות
        print("\n📋 מצב מיגרציות נוכחי:")
        call_command('showmigrations', 'workshop')
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בסימון המיגרציה: {e}")
        return False

if __name__ == "__main__":
    fake_migration()
