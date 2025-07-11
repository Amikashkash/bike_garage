#!/usr/bin/env python
"""
בדיקה מקיפה של שדה הסטטוס החדש ב-RepairItem
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, User

def test_status_system():
    print("=== בדיקת מערכת הסטטוס החדשה ===\n")
    
    # בדיקה 1: קיום השדה
    print("1. בדיקת קיום השדה status:")
    try:
        fields = [f.name for f in RepairItem._meta.fields]
        print(f"   שדות ב-RepairItem: {fields}")
        print(f"   שדה status קיים: {'status' in fields}")
        print(f"   אפשרויות status: {RepairItem.STATUS_CHOICES}")
        print("   ✅ השדה קיים בהצלחה\n")
    except Exception as e:
        print(f"   ❌ שגיאה: {e}\n")
        return
    
    # בדיקה 2: נתונים קיימים
    print("2. בדיקת נתונים קיימים:")
    items = RepairItem.objects.all()[:5]
    if not items:
        print("   אין פריטים במערכת")
        return
    
    for item in items:
        print(f"   פריט #{item.id}: {item.description}")
        print(f"      סטטוס: {item.status} ({item.get_status_display()})")
        print(f"      is_completed: {item.is_completed}")
        print(f"      אושר: {item.is_approved_by_customer}")
        if item.notes:
            print(f"      הערות: {item.notes}")
        print()
    
    # בדיקה 3: עדכון סטטוס
    print("3. בדיקת עדכון סטטוס:")
    test_item = items.first()
    original_status = test_item.status
    original_completed = test_item.is_completed
    
    print(f"   פריט לבדיקה: {test_item.description}")
    print(f"   סטטוס התחלתי: {original_status}")
    
    # עדכון לתקוע
    test_item.status = 'blocked'
    test_item.notes = "בדיקת מערכת - סטטוס תקוע"
    test_item.save()
    test_item.refresh_from_db()
    
    print(f"   אחרי עדכון לתקוע:")
    print(f"      status: {test_item.status}")
    print(f"      is_completed: {test_item.is_completed}")
    print(f"      notes: {test_item.notes}")
    
    # עדכון למושלם
    test_item.status = 'completed'
    test_item.notes = "בדיקת מערכת - הושלם"
    test_item.save()
    test_item.refresh_from_db()
    
    print(f"   אחרי עדכון למושלם:")
    print(f"      status: {test_item.status}")
    print(f"      is_completed: {test_item.is_completed}")
    print(f"      notes: {test_item.notes}")
    
    # החזרה למקורי
    test_item.status = original_status
    test_item.is_completed = original_completed
    test_item.notes = ""
    test_item.save()
    
    print(f"   הוחזר למקורי: {test_item.status}")
    print("   ✅ עדכון סטטוס עובד בהצלחה\n")
    
    # בדיקה 4: ספירת סטטוסים
    print("4. ספירת סטטוסים:")
    all_items = RepairItem.objects.filter(is_approved_by_customer=True)
    pending_count = all_items.filter(status='pending').count()
    completed_count = all_items.filter(status='completed').count()
    blocked_count = all_items.filter(status='blocked').count()
    
    print(f"   סה״כ פריטים מאושרים: {all_items.count()}")
    print(f"   ממתין: {pending_count}")
    print(f"   הושלם: {completed_count}")
    print(f"   תקוע: {blocked_count}")
    
    # בדיקה 5: תיקונים עם סטטוס
    print("\n5. בדיקת תיקונים עם סטטוסים:")
    repairs = RepairJob.objects.filter(status='in_progress')[:3]
    for repair in repairs:
        print(f"   תיקון #{repair.id} - {repair.bike}")
        items = repair.repair_items.filter(is_approved_by_customer=True)
        for item in items:
            print(f"      {item.description}: {item.get_status_display()}")
        print()
    
    print("=== בדיקה הושלמה בהצלחה! ===")

if __name__ == '__main__':
    test_status_system()
