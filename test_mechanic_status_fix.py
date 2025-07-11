#!/usr/bin/env python3
"""
🔧 בדיקה מהירה של תיקון שמירת סטטוס במסך עדכון ביצוע תיקון
"""

import os
import sys
import django

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import RepairJob, RepairItem, Customer, Bike

def test_mechanic_status_saving():
    print("=== בדיקת שמירת סטטוס פעולות תיקון ===")
    
    # חיפוש מכונאי
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    if not mechanic:
        print("❌ לא נמצא מכונאי במערכת")
        return
    
    print(f"✅ נמצא מכונאי: {mechanic.username}")
    
    # חיפוש תיקון שהוקצה למכונאי
    repair_job = RepairJob.objects.filter(
        assigned_mechanic=mechanic,
        status='in_progress'
    ).first()
    
    if not repair_job:
        print("❌ לא נמצא תיקון במצב 'in_progress' למכונאי")
        return
    
    print(f"✅ נמצא תיקון: #{repair_job.id}")
    
    # בדיקת פעולות
    approved_items = repair_job.repair_items.filter(is_approved_by_customer=True)
    print(f"📋 פעולות מאושרות: {approved_items.count()}")
    
    if not approved_items.exists():
        print("❌ אין פעולות מאושרות לבדיקה")
        return
    
    # הדמיית עדכון סטטוס
    for i, item in enumerate(approved_items[:3]):  # רק 3 הראשונות
        print(f"\n🔧 בודק פעולה {i+1}: {item.description}")
        print(f"   סטטוס נוכחי - מושלם: {item.is_completed}, חסום: {item.is_blocked}")
        print(f"   הערות נוכחיות: {item.notes or 'אין'}")
        
        # סימולציה של שינוי סטטוס
        if i == 0:
            item.is_completed = True
            item.is_blocked = False
            item.notes = "הושלם בהצלחה - בדיקת אוטומטית"
            status_text = "הושלם"
        elif i == 1:
            item.is_completed = False
            item.is_blocked = True
            item.notes = "חסר חלק - בדיקת אוטומטית"
            status_text = "חסום"
        else:
            item.is_completed = False
            item.is_blocked = False
            item.notes = "ממתין לביצוע - בדיקת אוטומטית"
            status_text = "ממתין"
        
        item.save()
        print(f"   ✅ עודכן ל: {status_text}")
        print(f"   📝 הערה חדשה: {item.notes}")
    
    print("\n🎯 סיכום:")
    completed = approved_items.filter(is_completed=True).count()
    blocked = approved_items.filter(is_blocked=True).count()
    pending = approved_items.filter(is_completed=False, is_blocked=False).count()
    
    print(f"   ✅ הושלמו: {completed}")
    print(f"   ❌ חסומות: {blocked}")
    print(f"   ⏳ ממתינות: {pending}")
    
    print("\n💡 כעת תוכל לבדוק במסך 'עדכון ביצוע תיקון' שהסטטוס וההערות נשמרים!")
    print(f"   🌐 URL: http://localhost:8000/mechanic/task-completion/{repair_job.id}/")

if __name__ == "__main__":
    test_mechanic_status_saving()
