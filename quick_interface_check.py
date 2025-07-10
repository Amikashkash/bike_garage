#!/usr/bin/env python
"""
יצירת סביבת בדיקה פשוטה לבדיקת ממשק הטכנאי
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

def check_current_interface():
    print("=== בדיקת ממשק הטכנאי הנוכחי ===")
    
    # איתור טכנאי ותיקון
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    if not mechanic:
        print("❌ לא נמצא טכנאי")
        return
        
    repair_job = RepairJob.objects.filter(assigned_mechanic=mechanic).first()
    if not repair_job:
        print("❌ לא נמצא תיקון")
        return
        
    print(f"✅ טכנאי: {mechanic.username}")
    print(f"✅ תיקון: {repair_job}")
    
    # בדיקת פעולות ממתינות
    pending_tasks = repair_job.repair_items.filter(
        is_approved_by_customer=True,
        is_completed=False,
        is_blocked=False
    )
    
    print(f"\n📋 פעולות ממתינות ({pending_tasks.count()}):")
    for task in pending_tasks:
        print(f"   🔧 {task.description} - ₪{task.price}")
        print(f"      📝 הערות קיימות: {task.notes or 'אין'}")
        print(f"      ⚠️ הערות חסימה: {task.block_notes or 'אין'}")
        print(f"      🚫 חסום: {'כן' if task.is_blocked else 'לא'}")
        print()
    
    # יצירת URL לבדיקה
    url = f"http://localhost:8000/mechanic/task/{repair_job.id}/"
    print(f"🌐 URL לבדיקה: {url}")
    print(f"👤 התחבר כ: {mechanic.username}")
    print()
    
    print("🔍 מה צריך לבדוק בממשק:")
    print("1. שיש כותרת: 'מה מונע מביצוע' במקום 'הערות / סיבת עיכוב'")
    print("2. שכאשר סומנים צ'קבוקס 'חסום' מופיע שדה 'מה מונע ממך להתקדם?'")
    print("3. שכאשר סומנים צ'קבוקס 'בוצע' מופיע שדה 'הערות נוספות (אופציונלי)'")
    print("4. שהפעולות החסומות מופיעות בטבלה נפרדת")

if __name__ == "__main__":
    check_current_interface()
