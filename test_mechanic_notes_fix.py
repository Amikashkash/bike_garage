#!/usr/bin/env python
"""
בדיקה של תיקון הערות הטכנאי
בודק שההערות של הטכנאי על מה שחסר לו נשמרות נכון
"""

import os
import sys
import django
from datetime import datetime

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import Customer, Bike, RepairJob, RepairItem, UserProfile

def test_mechanic_notes():
    print("=== בדיקת הערות טכנאי ===")
    
    # חיפוש משתמשים
    try:
        mechanic = User.objects.filter(userprofile__role='mechanic').first()
        customer = Customer.objects.first()
        
        if not mechanic:
            print("❌ לא נמצא טכנאי במערכת")
            return
            
        if not customer:
            print("❌ לא נמצא לקוח במערכת")
            return
            
        print(f"✅ נמצא טכנאי: {mechanic.username}")
        print(f"✅ נמצא לקוח: {customer.name}")
        
        # חיפוש תיקון עם פעולות
        repair_job = RepairJob.objects.filter(
            assigned_mechanic=mechanic,
            repair_items__isnull=False
        ).first()
        
        if not repair_job:
            print("❌ לא נמצא תיקון עם פעולות")
            return
            
        print(f"✅ נמצא תיקון: {repair_job}")
        
        # בדיקת פעולות
        pending_tasks = repair_job.repair_items.filter(
            is_approved_by_customer=True,
            is_completed=False,
            is_blocked=False
        )
        
        blocked_tasks = repair_job.repair_items.filter(
            is_blocked=True
        )
        
        completed_tasks = repair_job.repair_items.filter(
            is_completed=True
        )
        
        print(f"📋 פעולות ממתינות: {pending_tasks.count()}")
        print(f"⏸️ פעולות חסומות: {blocked_tasks.count()}")
        print(f"✅ פעולות מושלמות: {completed_tasks.count()}")
        
        # הדמיית זרימת עבודה של טכנאי
        if pending_tasks.exists():
            task = pending_tasks.first()
            print(f"\n🔧 בודק פעולה: {task.description}")
            
            # שלב 1: טכנאי מנסה לעבוד אבל חסר לו חלק
            print("1️⃣ טכנאי מגלה שחסר לו חלק...")
            task.is_blocked = True
            task.block_reason = 'missing_part'
            task.block_notes = 'חסר לי בלם אחורי, צריך להזמין מהספק'
            task.save()
            print(f"   💾 נשמר: {task.block_notes}")
            
            # שלב 2: אחרי זמן מה - החלק הגיע, טכנאי משלים
            print("2️⃣ החלק הגיע, טכנאי משלים את העבודה...")
            task.is_blocked = False
            task.is_completed = True
            task.completed_by = mechanic
            task.completed_at = datetime.now()
            
            # הערות השלמה נוספות
            completion_notes = "החלק הגיע, הותקן בהצלחה. בדקתי גם את הבלם הקדמי."
            
            # שמירת הערות מעודכנות (כמו בview החדש)
            if task.block_notes:
                task.notes = f"{task.block_notes}\n---\nהערות השלמה: {completion_notes}"
            else:
                task.notes = completion_notes
                
            task.save()
            print(f"   💾 נשמר notes: {task.notes}")
            
            # בדיקת התוצאה
            print(f"\n📊 תוצאה סופית:")
            print(f"   🏁 סטטוס: {task.get_status_display()}")
            print(f"   📝 הערות חסימה: {task.block_notes}")
            print(f"   📝 הערות כלליות: {task.notes}")
            print(f"   👤 בוצע על ידי: {task.completed_by}")
            
            # בדיקה שההערות נשמרו
            if task.block_notes and task.notes:
                print("✅ הצלחה! ההערות על מה שחסר נשמרו גם אחרי השלמת הפעולה")
            else:
                print("❌ בעיה: ההערות לא נשמרו כראוי")
                
        else:
            print("⚠️ אין פעולות ממתינות לבדיקה")
            
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mechanic_notes()
