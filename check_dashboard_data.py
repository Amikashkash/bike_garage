#!/usr/bin/env python
"""
סקריפט לבדיקת מה קורה בדשבורד מנהל
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob

def check_dashboard_data():
    print("🔍 בודק נתונים לדשבורד מנהל...")
    
    # בדיקת תיקונים תקועים
    stuck_repairs = RepairJob.objects.filter(is_stuck=True)
    print(f"🚨 תיקונים תקועים: {stuck_repairs.count()}")
    for repair in stuck_repairs:
        print(f"  - תיקון #{repair.id}: {repair.problem_description[:50]}...")
    
    # בדיקת תיקונים לפי סטטוס
    pending_diagnosis = RepairJob.objects.filter(status='reported')
    print(f"\n📋 ממתינים לאבחון: {pending_diagnosis.count()}")
    for repair in pending_diagnosis:
        print(f"  - תיקון #{repair.id}: {repair.problem_description[:50]}...")
    
    pending_approval = RepairJob.objects.filter(status='diagnosed')
    print(f"\n⏳ ממתינים לאישור לקוח: {pending_approval.count()}")
    for repair in pending_approval:
        print(f"  - תיקון #{repair.id}: {repair.problem_description[:50]}...")
    
    partially_approved = RepairJob.objects.filter(status='partially_approved')
    print(f"\n✅ אושרו חלקית: {partially_approved.count()}")
    for repair in partially_approved:
        print(f"  - תיקון #{repair.id}: {repair.problem_description[:50]}...")
    
    in_progress = RepairJob.objects.filter(status__in=['approved', 'in_progress'])
    print(f"\n🔧 בביצוע: {in_progress.count()}")
    for repair in in_progress:
        print(f"  - תיקון #{repair.id}: {repair.problem_description[:50]}... [מכונאי: {repair.assigned_mechanic}]")
    
    # סה"כ נתונים
    total_repairs = RepairJob.objects.count()
    print(f"\n📊 סה\"כ תיקונים במערכת: {total_repairs}")
    
    if total_repairs == 0:
        print("\n❌ אין תיקונים במערכת!")
        print("💡 הרץ את create_manager_dashboard_demo.py ליצירת נתוני דמו")
    elif stuck_repairs.count() == 0 and pending_diagnosis.count() == 0 and pending_approval.count() == 0 and partially_approved.count() == 0 and in_progress.count() == 0:
        print("\n⚠️ יש תיקונים במערכת אבל לא בסטטוסים הנכונים לדשבורד!")
        print("📋 סטטוסי תיקונים קיימים:")
        for status_code, status_name in RepairJob.STATUS_CHOICES:
            count = RepairJob.objects.filter(status=status_code).count()
            if count > 0:
                print(f"  - {status_name}: {count}")

if __name__ == "__main__":
    check_dashboard_data()
