#!/usr/bin/env python
"""
בדיקה מהירה של דשבורד מנהל
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem

def debug_dashboard():
    print("🔍 בדיקת דשבורד מנהל...")
    
    # בדיקת תיקונים בסטטוס in_progress/approved
    in_progress = RepairJob.objects.filter(status__in=['approved', 'in_progress'])
    print(f"\n📊 תיקונים בביצוע: {in_progress.count()}")
    
    for repair in in_progress:
        print(f"\n🔧 תיקון #{repair.id}:")
        print(f"  - סטטוס: {repair.status}")
        print(f"  - תקוע: {repair.is_stuck}")
        print(f"  - מכונאי: {repair.assigned_mechanic}")
        
        # בדיקת פעולות
        repair_items = repair.repair_items.all()
        print(f"  - פעולות: {repair_items.count()}")
        
        if repair_items.count() > 0:
            approved_count = repair.approved_items.count()
            completed_count = repair.completed_items.count()
            blocked_count = repair.blocked_items.count()
            
            print(f"  - מאושרות: {approved_count}")
            print(f"  - הושלמו: {completed_count}") 
            print(f"  - חסומות: {blocked_count}")
            print(f"  - אחוז התקדמות: {repair.progress_percentage}%")
            print(f"  - תקוע למעשה: {repair.is_effectively_stuck}")
        else:
            print(f"  - אין פעולות! (זה יכול להיות הבעיה)")
    
    # בדיקת תיקונים תקועים מפורשים
    stuck_repairs = RepairJob.objects.filter(is_stuck=True)
    print(f"\n🚨 תיקונים תקועים מפורשים: {stuck_repairs.count()}")
    for repair in stuck_repairs:
        print(f"  - תיקון #{repair.id}: {repair.stuck_reason}")

if __name__ == "__main__":
    debug_dashboard()
