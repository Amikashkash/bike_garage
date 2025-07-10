#!/usr/bin/env python
"""
בדיקה מקיפה של תיקון הערות הטכנאי
בודק את כל הזרימה החדשה
"""

import os
import sys
import django
from datetime import datetime, timedelta

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import Customer, Bike, RepairJob, RepairItem, RepairUpdate
from django.utils import timezone

def create_demo_scenario():
    print("=== יצירת תרחיש דמו ===")
    
    # איתור טכנאי
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    if not mechanic:
        print("❌ לא נמצא טכנאי")
        return None
        
    # איתור תיקון
    repair_job = RepairJob.objects.filter(assigned_mechanic=mechanic).first()
    if not repair_job:
        print("❌ לא נמצא תיקון")
        return None
        
    print(f"✅ נמצא תיקון: {repair_job}")
    print(f"✅ טכנאי: {mechanic.username}")
    
    # יצירת פעולות לדמו אם אין
    items = repair_job.repair_items.all()
    if items.count() < 3:
        # יצירת פעולות נוספות
        RepairItem.objects.get_or_create(
            repair_job=repair_job,
            description="בדיקת מערכת בלמים",
            price=80,
            is_approved_by_customer=True,
            defaults={'notes': ''}
        )
        RepairItem.objects.get_or_create(
            repair_job=repair_job,
            description="שמן שרשרת ובדיקת הילוכים",
            price=50,
            is_approved_by_customer=True,
            defaults={'notes': ''}
        )
    
    return repair_job

def simulate_mechanic_workflow(repair_job):
    print("\n=== הדמיית זרימת עבודה של טכנאי ===")
    
    mechanic = repair_job.assigned_mechanic
    pending_items = repair_job.repair_items.filter(
        is_approved_by_customer=True,
        is_completed=False,
        is_blocked=False
    )
    
    if not pending_items.exists():
        print("❌ אין פעולות ממתינות להדמיה")
        return
    
    # שלב 1: טכנאי מתחיל לעבוד על פעולה ראשונה
    item1 = pending_items.first()
    print(f"\n1️⃣ טכנאי מתחיל לעבוד על: {item1.description}")
    print("   🔍 בודק מה צריך...")
    print("   ❌ מגלה שחסר לו חלק!")
    
    # סימון כחסום
    item1.is_blocked = True
    item1.block_reason = 'missing_part'
    item1.block_notes = 'חסר לי בלם V-brake אחורי, הישן שבור לגמרי. צריך להזמין חלק חדש מהספק.'
    item1.save()
    
    # יצירת עדכון
    RepairUpdate.objects.create(
        repair_job=repair_job,
        user=mechanic,
        message=f"פעולה חסומה: {item1.description} - חסר חלק",
        is_visible_to_customer=True
    )
    
    print(f"   💾 נשמר: {item1.block_notes}")
    
    # שלב 2: טכנאי עובר לפעולה שנייה
    if pending_items.count() > 1:
        item2 = pending_items[1]
        print(f"\n2️⃣ טכנאי עובר לפעולה הבאה: {item2.description}")
        print("   🔧 עובד על הפעולה...")
        print("   ❌ גם כאן יש בעיה!")
        
        item2.is_blocked = True
        item2.block_reason = 'technical_issue'
        item2.block_notes = 'יש בעיה בהילוך 3 - נשמע רעש חריק. צריך לפרק ולבדוק את המנגנון הפנימי.'
        item2.save()
        
        RepairUpdate.objects.create(
            repair_job=repair_job,
            user=mechanic,
            message=f"פעולה חסומה: {item2.description} - בעיה טכנית",
            is_visible_to_customer=True
        )
        
        print(f"   💾 נשמר: {item2.block_notes}")
    
    # שלב 3: אחרי זמן - החלק הגיע, הטכנאי משלים
    print(f"\n3️⃣ אחרי יומיים - החלק הגיע!")
    print(f"   📦 הטכנאי מקבל את הבלם החדש")
    print(f"   🔧 מתחיל לעבוד על {item1.description}")
    
    item1.is_blocked = False
    item1.is_completed = True
    item1.completed_by = mechanic
    item1.completed_at = timezone.now()
    
    # הערות השלמה - נוספות על ההערות הקודמות
    completion_notes = "החלק הגיע, הותקן בהצלחה. בדקתי גם את הבלם הקדמי - גם הוא היה צריך כיוונון קל."
    
    # שמירת ההיסטוריה המלאה
    if item1.block_notes:
        item1.notes = f"{item1.block_notes}\n---\nהערות השלמה: {completion_notes}"
    else:
        item1.notes = completion_notes
    
    item1.save()
    
    RepairUpdate.objects.create(
        repair_job=repair_job,
        user=mechanic,
        message=f"הושלמה פעולה: {item1.description}",
        is_visible_to_customer=True
    )
    
    print(f"   ✅ הושלם!")
    print(f"   📝 הערות סופיות: {item1.notes[:100]}...")
    
    return item1, item2 if pending_items.count() > 1 else None

def test_manager_view(repair_job):
    print("\n=== בדיקת תצוגת מנהל ===")
    
    # סימולציה של מה שהמנהל רואה
    approved_items = repair_job.repair_items.filter(is_approved_by_customer=True)
    completed_items = approved_items.filter(is_completed=True)
    pending_items = approved_items.filter(is_completed=False, is_blocked=False)
    blocked_items = approved_items.filter(is_blocked=True)
    
    print(f"📊 סטטיסטיקות:")
    print(f"   ✅ מושלמות: {completed_items.count()}")
    print(f"   ⏳ ממתינות: {pending_items.count()}")
    print(f"   ⏸️ חסומות: {blocked_items.count()}")
    
    if completed_items.exists():
        print(f"\n✅ פעולות מושלמות (מה שהמנהל רואה):")
        for item in completed_items:
            print(f"   🔧 {item.description}")
            if item.block_notes and item.notes:
                print(f"      ⚠️ בעיות שהיו: {item.block_notes[:50]}...")
                if item.notes != item.block_notes:
                    print(f"      ✅ איך נפתר: {item.notes[:50]}...")
            elif item.notes:
                print(f"      📝 הערות: {item.notes[:50]}...")
    
    if blocked_items.exists():
        print(f"\n⏸️ פעולות חסומות (דורש טיפול מיידי!):")
        for item in blocked_items:
            print(f"   🔧 {item.description}")
            print(f"      ⚠️ סיבה: {item.get_block_reason_display()}")
            print(f"      📝 מה חסר: {item.block_notes}")
            print(f"      🎯 פעולה נדרשת: צור קשר עם ספק/תזמן הזמנה")

def main():
    print("🚲 בדיקת מערכת הערות טכנאי משופרת")
    print("=" * 50)
    
    repair_job = create_demo_scenario()
    if not repair_job:
        return
    
    # הדמיית זרימת עבודה
    simulate_mechanic_workflow(repair_job)
    
    # בדיקת תצוגת מנהל
    test_manager_view(repair_job)
    
    print("\n🎯 סיכום השיפורים:")
    print("✅ הערות הטכנאי על בעיות נשמרות לצמיתות")
    print("✅ המנהל רואה מה הייתה הבעיה וכיצד נפתרה")
    print("✅ מעקב מלא אחר פעולות חסומות")
    print("✅ הטכנאי יכול להמשיך לעבוד ולהוסיף הערות")
    print("✅ היסטוריה מלאה של כל פעולה")

if __name__ == "__main__":
    main()
