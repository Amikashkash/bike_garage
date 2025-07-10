#!/usr/bin/env python
"""
הדמיה של זרימת העבודה החדשה - הערות טכנאי משופרות
"""

import os
import sys
import django

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import RepairJob, RepairItem

def demo_new_workflow():
    print("=== הדמיית זרימת עבודה חדשה - הערות טכנאי ===")
    print()
    
    # חיפוש דוגמה
    repair_job = RepairJob.objects.filter(repair_items__isnull=False).first()
    if not repair_job:
        print("❌ לא נמצא תיקון לדוגמה")
        return
        
    print(f"🚲 תיקון: {repair_job}")
    print(f"📋 לקוח: {repair_job.bike.customer.name}")
    print()
    
    # הצגת הפעולות
    pending_tasks = repair_job.repair_items.filter(
        is_approved_by_customer=True,
        is_completed=False,
        is_blocked=False
    )
    
    blocked_tasks = repair_job.repair_items.filter(is_blocked=True)
    completed_tasks = repair_job.repair_items.filter(is_completed=True)
    
    print("📊 סטטוס פעולות:")
    print(f"   ⏳ ממתינות: {pending_tasks.count()}")
    print(f"   ⏸️ חסומות: {blocked_tasks.count()}")
    print(f"   ✅ מושלמות: {completed_tasks.count()}")
    print()
    
    # הצגת פעולות חסומות
    if blocked_tasks.exists():
        print("⏸️ פעולות חסומות:")
        for task in blocked_tasks:
            print(f"   🔧 {task.description}")
            print(f"      💰 ₪{task.price}")
            print(f"      ⚠️ סיבה: {task.get_block_reason_display()}")
            if task.block_notes:
                print(f"      📝 הערות: {task.block_notes}")
            print()
    
    # הצגת פעולות מושלמות עם ההיסטוריה המלאה
    if completed_tasks.exists():
        print("✅ פעולות מושלמות:")
        for task in completed_tasks:
            print(f"   🔧 {task.description}")
            print(f"      💰 ₪{task.price}")
            print(f"      👤 בוצע על ידי: {task.completed_by}")
            print(f"      📅 הושלם: {task.completed_at.strftime('%d/%m/%Y %H:%M') if task.completed_at else 'לא צוין'}")
            
            # הצגת ההיסטוריה המלאה של ההערות
            if task.block_notes and task.notes:
                print(f"      📋 הערות מהטכנאי:")
                if task.block_notes:
                    print(f"         ⚠️ בעיות שהיו: {task.block_notes}")
                if task.notes != task.block_notes:
                    print(f"         ✅ הערות השלמה: {task.notes}")
            elif task.notes:
                print(f"      📝 הערות: {task.notes}")
            elif task.block_notes:
                print(f"      📝 הערות: {task.block_notes}")
            print()
    
    # הצגת פעולות ממתינות
    if pending_tasks.exists():
        print("⏳ פעולות ממתינות:")
        for task in pending_tasks:
            print(f"   🔧 {task.description}")
            print(f"      💰 ₪{task.price}")
            
            # הצגת הערות קודמות אם יש
            if task.block_notes or task.notes:
                print(f"      📋 הערות קודמות:")
                if task.block_notes:
                    print(f"         ⚠️ {task.block_notes}")
                if task.notes and task.notes != task.block_notes:
                    print(f"         ℹ️ {task.notes}")
            print()
    
    print("💡 שיפורים חדשים:")
    print("   • הערות הטכנאי נשמרות לצמיתות")
    print("   • ההיסטוריה של בעיות ופתרונות נראית למנהל")
    print("   • טכנאי יכול לכתב מה חסר לו או מה מונע ממנו להתקדם")
    print("   • המנהל רואה את כל המידע הדרוש לקבלת החלטות")

if __name__ == "__main__":
    demo_new_workflow()
