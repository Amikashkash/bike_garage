#!/usr/bin/env python3
"""
הוספת הערות נוספות לבדיקת התצוגה
"""

import os
import sys
import django

# הגדרת נתיב Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem

def add_test_notes():
    """הוספת הערות דמו לבדיקת התצוגה"""
    
    try:
        repair_job = RepairJob.objects.get(id=9)
        items = repair_job.repair_items.all()
        
        if items.exists():
            # הערה ארוכה יותר לבדיקת התצוגה
            first_item = items.first()
            first_item.notes = """זהו דוגמה להערה ארוכה יותר של מכונאי.
            
ההערה הזו כוללת:
• פירוט על הבעיה שנתגלתה
• הסבר על הפתרון שיושם
• המלצות לעתיד
• הערות נוספות חשובות

הבעיה הייתה מורכבת יותר מהצפוי ונדרשו כמה ניסיונות לפתרון. בסוף הצלחנו לפתור את הבעיה אבל יש לשים לב לנקודות הבאות בעתיד."""
            first_item.save()
            
            # הערה קצרה לבדיקה
            if len(items) > 1:
                second_item = items[1]
                second_item.notes = "בעיה קטנה - נפתרה בקלות."
                second_item.save()
            
            print("✅ הוספו הערות דמו לבדיקת התצוגה")
            print(f"🔗 בדוק בכתובת: http://127.0.0.1:8000/workshop/repair/{repair_job.id}/status/")
        else:
            print("❌ לא נמצאו פריטי תיקון")
            
    except RepairJob.DoesNotExist:
        print("❌ לא נמצא תיקון #9")

if __name__ == '__main__':
    add_test_notes()
