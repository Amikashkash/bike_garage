#!/usr/bin/env python
"""
בדיקת הלוגיקה החדשה לזיהוי תיקונים תקועים
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob

def check_stuck_logic():
    print("=== בדיקת לוגיקת זיהוי תיקונים תקועים ===\n")
    
    # בדיקת תיקון #10 ספציפית
    try:
        repair = RepairJob.objects.get(id=10)
        print(f"תיקון #{repair.id} - {repair.bike}")
        print(f"מכונאי: {repair.assigned_mechanic}")
        print(f"סטטוס: {repair.status}")
        
        # בדיקת פעולות
        approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        completed_items = approved_items.filter(status='completed')
        blocked_items = approved_items.filter(status='blocked')
        
        print(f"\nפעולות:")
        print(f"  מאושרות: {approved_items.count()}")
        print(f"  הושלמו: {completed_items.count()}")
        print(f"  תקועות: {blocked_items.count()}")
        
        # חישוב התקדמות
        progress = (completed_items.count() / approved_items.count() * 100) if approved_items.count() > 0 else 0
        print(f"  אחוז התקדמות: {progress:.1f}%")
        
        # בדיקת תקיעות
        is_repair_stuck = getattr(repair, 'is_stuck', False)
        has_blocked_items = blocked_items.count() > 0
        is_effectively_stuck = is_repair_stuck or has_blocked_items
        
        print(f"\nסטטוס תקיעות:")
        print(f"  התיקון כולו תקוע (is_stuck): {is_repair_stuck}")
        print(f"  יש פעולות תקועות: {has_blocked_items}")
        print(f"  תקוע למעשה (is_effectively_stuck): {is_effectively_stuck}")
        
        # קטגוריזציה
        print(f"\nקטגוריזציה:")
        if is_effectively_stuck:
            print("  ✅ אמור להופיע ב: משימות תקועות")
        elif progress == 0:
            print("  ✅ אמור להופיע ב: משימות ממתינות להתחלה")
        elif 0 < progress < 100:
            print("  ✅ אמור להופיע ב: משימות בביצוע פעיל")
        else:
            print("  ✅ הושלם")
        
        # פרטי פעולות תקועות
        if blocked_items.count() > 0:
            print(f"\nפעולות תקועות:")
            for item in blocked_items:
                print(f"  • {item.description}")
                if item.notes:
                    print(f"    הערות: {item.notes}")
        
    except RepairJob.DoesNotExist:
        print("תיקון #10 לא נמצא")
    
    print("\n" + "="*50)
    
    # בדיקה כללית של כל התיקונים בביצוע
    print("\nבדיקה כללית:")
    in_progress = RepairJob.objects.filter(status__in=['approved', 'in_progress'])
    
    waiting_count = 0
    active_count = 0
    stuck_count = 0
    
    for repair in in_progress:
        approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        completed_items = approved_items.filter(status='completed')
        blocked_items = approved_items.filter(status='blocked')
        
        progress = (completed_items.count() / approved_items.count() * 100) if approved_items.count() > 0 else 0
        is_repair_stuck = getattr(repair, 'is_stuck', False)
        has_blocked_items = blocked_items.count() > 0
        is_effectively_stuck = is_repair_stuck or has_blocked_items
        
        if is_effectively_stuck:
            stuck_count += 1
            print(f"תקוע: #{repair.id} ({'כל התיקון' if is_repair_stuck else f'{blocked_items.count()} פעולות'})")
        elif progress == 0:
            waiting_count += 1
        elif 0 < progress < 100:
            active_count += 1
    
    print(f"\nסיכום:")
    print(f"ממתינות להתחלה: {waiting_count}")
    print(f"בעבודה פעילה: {active_count}")
    print(f"תקועות: {stuck_count}")
    print(f"סה\"כ: {waiting_count + active_count + stuck_count}")

if __name__ == '__main__':
    check_stuck_logic()
