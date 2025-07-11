#!/usr/bin/env python
"""
סקריפט לבדיקה - סימון פעולה כתקועה
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem

def test_mark_as_blocked():
    print("=== בדיקת סימון פעולה כתקועה ===\n")
    
    # חיפוש תיקון #10
    try:
        repair = RepairJob.objects.get(id=10)
        print(f"תיקון #{repair.id} - {repair.bike}")
        
        # חיפוש פעולה מאושרת שאפשר לסמן כתקועה
        approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        
        if approved_items:
            test_item = approved_items.first()
            print(f"פעולה לבדיקה: {test_item.description}")
            print(f"סטטוס נוכחי: {test_item.status}")
            print(f"הערות נוכחיות: {test_item.notes or 'אין'}")
            
            # סימון כתקוע
            print("\nמסמן כתקוע...")
            test_item.status = 'blocked'
            test_item.notes = "בדיקת מערכת - חסר חלק חילוף"
            test_item.save()
            
            print("נשמר!")
            print(f"סטטוס חדש: {test_item.status}")
            print(f"הערות חדשות: {test_item.notes}")
            print(f"is_completed: {test_item.is_completed}")
            
            # בדיקת איך זה משפיע על התיקון
            blocked_items = repair.repair_items.filter(is_approved_by_customer=True, status='blocked')
            print(f"\nסה\"כ פעולות תקועות בתיקון: {blocked_items.count()}")
            
            print("\n✅ הפעולה סומנה כתקועה!")
            print("🔍 כעת המנהל אמור לראות את התיקון במשימות תקועות")
            
        else:
            print("אין פעולות מאושרות בתיקון זה")
            
    except RepairJob.DoesNotExist:
        print("תיקון #10 לא נמצא")

if __name__ == '__main__':
    test_mark_as_blocked()
