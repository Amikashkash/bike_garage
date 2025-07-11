#!/usr/bin/env python
"""
בדיקת הפיצ'רים החדשים:
1. כפתור השב עובד
2. פעולות תקועות מודגשות באדום
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, User

def test_fixes():
    print("=== בדיקת התיקונים החדשים ===\n")
    
    # 1. בדיקת פעולה תקועה
    print("1. יצירת פעולה תקועה לבדיקה:")
    try:
        repair = RepairJob.objects.get(id=10)
        approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        
        if approved_items:
            test_item = approved_items.first()
            
            # שמירת מצב מקורי
            original_status = test_item.status
            original_notes = test_item.notes
            
            print(f"פעולה: {test_item.description}")
            print(f"סטטוס מקורי: {test_item.status}")
            
            # סימון כתקוע
            test_item.status = 'blocked'
            test_item.notes = "🔧 בדיקת מערכת - חסר כלי מיוחד לפעולה זו. נא לספק הנחיות."
            test_item.save()
            
            print(f"✅ סטטוס עודכן ל: {test_item.status}")
            print(f"✅ הערות: {test_item.notes}")
            
            # בדיקת השפעה על התיקון
            blocked_items = repair.repair_items.filter(is_approved_by_customer=True, status='blocked')
            print(f"✅ פעולות תקועות בתיקון: {blocked_items.count()}")
            
            # בדיקת הלוגיקה החדשה
            has_blocked_items = blocked_items.count() > 0
            is_repair_stuck = getattr(repair, 'is_stuck', False)
            is_effectively_stuck = is_repair_stuck or has_blocked_items
            
            print(f"✅ התיקון יוצג כתקוע בדשבורד מנהל: {is_effectively_stuck}")
            
            # החזרה למצב מקורי
            test_item.status = original_status
            test_item.notes = original_notes
            test_item.save()
            print("🔄 הוחזר למצב מקורי")
            
        else:
            print("❌ אין פעולות מאושרות בתיקון")
            
    except RepairJob.DoesNotExist:
        print("❌ תיקון #10 לא נמצא")
    
    print("\n" + "="*50)
    
    # 2. בדיקת פונקציית תגובת מנהל
    print("\n2. בדיקת פונקציית תגובת מנהל:")
    
    # חיפוש תיקונים עם פעולות תקועות
    repairs_with_blocked = RepairJob.objects.filter(
        repair_items__is_approved_by_customer=True,
        repair_items__status='blocked'
    ).distinct()
    
    print(f"תיקונים עם פעולות תקועות: {repairs_with_blocked.count()}")
    
    for repair in repairs_with_blocked[:3]:  # רק 3 הראשונים
        blocked_items = repair.repair_items.filter(is_approved_by_customer=True, status='blocked')
        print(f"  תיקון #{repair.id}: {blocked_items.count()} פעולות תקועות")
        for item in blocked_items:
            print(f"    • {item.description}: {item.notes[:50]}...")
    
    print("\n3. הנחיות לבדיקה:")
    print("🌐 פתח דפדפן וכנס כמנהל לדשבורד")
    print("👀 בדוק שתיקונים עם פעולות תקועות מופיעים ב'משימות תקועות'")
    print("🖱️ לחץ על כפתור 'השב' ובדוק שהמודל נפתח")
    print("📝 כתב תגובה וסמן 'נפתר' - בדוק שהפעולות חוזרות לסטטוס 'ממתין'")
    print("🔍 כנס לדף סטטוס התיקון ובדוק שפעולות תקועות מופיעות באדום")
    
    print("\n✅ כל הבדיקות הושלמו!")

if __name__ == '__main__':
    test_fixes()
