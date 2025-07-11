#!/usr/bin/env python
"""
בדיקת דשבורד מנהל עם החלוקה החדשה לקטגוריות
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, User

def test_manager_dashboard_categories():
    print("=== בדיקת קטגוריות דשבורד מנהל ===\n")
    
    # בדיקת תיקונים בביצוע
    in_progress = RepairJob.objects.filter(status__in=['approved', 'in_progress']).select_related('bike', 'bike__customer', 'assigned_mechanic').prefetch_related('repair_items')
    
    print(f"סה״כ תיקונים בביצוע: {in_progress.count()}")
    
    if not in_progress:
        print("אין תיקונים בביצוע למעקב")
        return
    
    waiting_count = 0
    active_count = 0
    stuck_count = 0
    
    for repair in in_progress:
        # הוספת מידע על התקדמות
        repair.approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        repair.completed_items = repair.repair_items.filter(is_approved_by_customer=True, status='completed')
        repair.blocked_items = repair.repair_items.filter(is_approved_by_customer=True, status='blocked')
        repair.pending_items = repair.repair_items.filter(is_approved_by_customer=True, status='pending')
        
        approved_count = repair.approved_items.count()
        completed_count = repair.completed_items.count()
        blocked_count = repair.blocked_items.count()
        pending_count = repair.pending_items.count()
        
        repair.progress_percentage = (completed_count / approved_count * 100) if approved_count > 0 else 0
        
        is_stuck = getattr(repair, 'is_stuck', False)
        
        print(f"\n--- תיקון #{repair.id} - {repair.bike} ---")
        print(f"מכונאי: {repair.assigned_mechanic.get_full_name() if repair.assigned_mechanic else 'לא הוקצה'}")
        print(f"פעולות מאושרות: {approved_count}")
        print(f"הושלמו: {completed_count}")
        print(f"תקועות: {blocked_count}")
        print(f"ממתינות: {pending_count}")
        print(f"התקדמות: {repair.progress_percentage:.1f}%")
        print(f"תקוע (כל התיקון): {is_stuck}")
        
        # קטגוריזציה
        if is_stuck:
            stuck_count += 1
            print("📍 קטגוריה: משימות תקועות")
        elif repair.progress_percentage == 0:
            waiting_count += 1
            print("📍 קטגוריה: משימות ממתינות להתחלה")
        elif 0 < repair.progress_percentage < 100:
            active_count += 1
            print("📍 קטגוריה: משימות בביצוע פעיל")
        else:
            print("📍 קטגוריה: הושלם (לא אמור להיות כאן)")
    
    print("\n=== סיכום קטגוריות ===")
    print(f"🔸 ממתינות להתחלה: {waiting_count}")
    print(f"🔹 בביצוע פעיל: {active_count}")
    print(f"🔴 תקועות: {stuck_count}")
    print(f"📊 סה״כ: {waiting_count + active_count + stuck_count}")
    
    # בדיקת פריטים פרטניים עם סטטוס blocked
    print("\n=== פריטים תקועים בפרט ===")
    all_blocked_items = RepairItem.objects.filter(
        is_approved_by_customer=True,
        status='blocked',
        repair_job__status__in=['approved', 'in_progress']
    ).select_related('repair_job', 'repair_job__bike')
    
    if all_blocked_items:
        for item in all_blocked_items:
            print(f"🔴 תיקון #{item.repair_job.id}: {item.description}")
            print(f"   הערות: {item.notes}")
    else:
        print("אין פריטים תקועים בפרט")

if __name__ == '__main__':
    test_manager_dashboard_categories()
