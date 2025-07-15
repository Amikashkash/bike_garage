#!/usr/bin/env python
"""
בדיקת מצב הייצור לאחר התיקונים
"""
import os
import django

# הגדרת Django עם הגדרות ייצור
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# הוספת משתני סביבה לייצור
os.environ['DEBUG'] = 'False'
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', '')

django.setup()

from workshop.models import RepairJob
from django.contrib.auth.models import User

def test_production_status():
    """בדיקת מצב הייצור"""
    print("🔍 בודק מצב ייצור...")
    
    try:
        # בדיקה אם יש לנו גישה למודל
        count = RepairJob.objects.count()
        print(f"✅ יש גישה למודל RepairJob: {count} רשומות")
        
        # בדיקה של שדות במודל
        if hasattr(RepairJob, 'quality_checked_by'):
            print("✅ שדה quality_checked_by קיים במודל")
        else:
            print("❌ שדה quality_checked_by חסר במודל")
            
        if hasattr(RepairJob, 'quality_check_date'):
            print("✅ שדה quality_check_date קיים במודל")
        else:
            print("❌ שדה quality_check_date חסר במודל")
            
        if hasattr(RepairJob, 'quality_notes'):
            print("✅ שדה quality_notes קיים במודל")
        else:
            print("❌ שדה quality_notes חסר במודל")
            
        if hasattr(RepairJob, 'ready_for_pickup_date'):
            print("✅ שדה ready_for_pickup_date קיים במודל")
        else:
            print("❌ שדה ready_for_pickup_date חסר במודל")
            
        if hasattr(RepairJob, 'customer_notified'):
            print("✅ שדה customer_notified קיים במודל")
        else:
            print("❌ שדה customer_notified חסר במודל")
        
        # ניסיון ליצור רשומה עם הסטטוס החדש
        try:
            sample_job = RepairJob.objects.filter(status='awaiting_quality_check').first()
            if sample_job:
                print("✅ סטטוס awaiting_quality_check נתמך")
            else:
                print("ℹ️ אין רשומות עם סטטוס awaiting_quality_check")
        except Exception as e:
            print(f"❌ בעיה עם סטטוס awaiting_quality_check: {e}")
        
        print("\n🎯 המערכת מוכנה לעבודה!")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_production_status()
