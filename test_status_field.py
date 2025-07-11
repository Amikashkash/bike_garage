#!/usr/bin/env python
import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, Customer, Bike, User
from django.utils import timezone

def test_status_field():
    """בדיקת השדה החדש status ב-RepairItem"""
    
    print("=== בדיקת שדה status החדש ב-RepairItem ===")
    
    # חיפוש תיקון קיים
    repair_jobs = RepairJob.objects.all().order_by('-id')[:3]
    
    if not repair_jobs:
        print("לא נמצאו תיקונים במערכת")
        return
    
    for job in repair_jobs:
        print(f"\n--- תיקון #{job.id} - {job.bike} ---")
        items = job.repair_items.all()
        
        if not items:
            print("אין פעולות בתיקון זה")
            continue
            
        for item in items:
            print(f"פעולה: {item.description}")
            print(f"  מחיר: ₪{item.price}")
            print(f"  סטטוס חדש: {item.status} ({item.get_status_display()})")
            print(f"  סטטוס ישן (is_completed): {item.is_completed}")
            print(f"  אושר: {item.is_approved_by_customer}")
            if item.notes:
                print(f"  הערות: {item.notes}")
            print()
    
    # בדיקת עדכון סטטוס
    first_job = repair_jobs.first()
    if first_job:
        items = first_job.repair_items.filter(is_approved_by_customer=True)
        if items:
            test_item = items.first()
            print(f"=== בדיקת עדכון סטטוס לפעולה: {test_item.description} ===")
            
            # בדיקת סטטוס התחלתי
            print(f"סטטוס התחלתי: {test_item.status}")
            
            # עדכון לתקוע
            print("מעדכן לסטטוס 'תקוע'...")
            test_item.status = 'blocked'
            test_item.notes = "בדיקת מערכת - פעולה תקועה"
            test_item.save()
            
            # בדיקת השמירה
            test_item.refresh_from_db()
            print(f"סטטוס אחרי עדכון: {test_item.status}")
            print(f"הערות: {test_item.notes}")
            print(f"is_completed (אמור להיות False): {test_item.is_completed}")
            
            # עדכון לבוצע
            print("\nמעדכן לסטטוס 'בוצע'...")
            test_item.status = 'completed'
            test_item.notes = "בדיקת מערכת - פעולה הושלמה"
            test_item.save()
            
            # בדיקת השמירה
            test_item.refresh_from_db()
            print(f"סטטוס אחרי עדכון: {test_item.status}")
            print(f"הערות: {test_item.notes}")
            print(f"is_completed (אמור להיות True): {test_item.is_completed}")
            
            # החזרה לממתין
            print("\nמחזיר לסטטוס 'ממתין'...")
            test_item.status = 'pending'
            test_item.notes = ""
            test_item.save()
            
            test_item.refresh_from_db()
            print(f"סטטוס סופי: {test_item.status}")
            print(f"is_completed (אמור להיות False): {test_item.is_completed}")
    
    print("\n=== סיום בדיקת שדה status ===")

if __name__ == '__main__':
    test_status_field()
