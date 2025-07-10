#!/usr/bin/env python
"""
בדיקה מהירה - איך נראה הממשק של הטכנאי בפועל
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

def check_template_status():
    print("=== בדיקת סטטוס התבנית ===")
    
    # איתור נתונים
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    repair_job = RepairJob.objects.filter(assigned_mechanic=mechanic).first()
    
    if not repair_job:
        print("❌ לא נמצא תיקון")
        return
    
    # יצירת context כמו ב-view
    pending_tasks = repair_job.repair_items.filter(
        is_approved_by_customer=True,
        is_completed=False,
        is_blocked=False
    )
    
    print(f"✅ תיקון: {repair_job}")
    print(f"✅ משימות ממתינות: {pending_tasks.count()}")
    
    # קריאת התבנית הנוכחית
    try:
        with open('c:\\bikegarage\\workshop\\templates\\workshop\\mechanic_task.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # חיפוש המילות המפתח החדשות
        print("\n🔍 בדיקת תוכן התבנית:")
        
        if 'מה מונע ממך להתקדם' in template_content:
            print("✅ 'מה מונע ממך להתקדם' - קיים")
        else:
            print("❌ 'מה מונע ממך להתקדם' - לא קיים")
            
        if 'מה מונע מביצוע' in template_content:
            print("✅ 'מה מונע מביצוע' - קיים בכותרת")
        else:
            print("❌ 'מה מונע מביצוע' - לא קיים בכותרת")
            
        if 'הערות נוספות (אופציונלי)' in template_content:
            print("✅ 'הערות נוספות (אופציונלי)' - קיים")
        else:
            print("❌ 'הערות נוספות (אופציונלי)' - לא קיים")
            
        if 'אם יש בעיה או חסר משהו - סמן כ"חסום" וכתב מה חסר' in template_content:
            print("✅ הסבר בכותרת - קיים")
        else:
            print("❌ הסבר בכותרת - לא קיים")
            
    except Exception as e:
        print(f"❌ שגיאה בקריאת התבנית: {e}")
    
    # מידע לבדיקה ידנית
    if pending_tasks.exists():
        print(f"\n🌐 לבדיקה ידנית:")
        print(f"URL: http://localhost:8000/mechanic/task/{repair_job.id}/")
        print(f"משתמש: {mechanic.username}")
        print(f"סיסמה: mechanic123")
        
        print(f"\n🎯 מה לחפש בדף:")
        print(f"1. בכותרת הטבלה: 'הערות / מה מונע מביצוע'")
        print(f"2. כשמסמנים 'חסום': 'מה מונע ממך להתקדם?'")
        print(f"3. כשמסמנים 'בוצע': 'הערות נוספות (אופציונלי)'")
        print(f"4. בכותרת הכרטיס: 'אם יש בעיה או חסר משהו - סמן כ\"חסום\" וכתב מה חסר'")

if __name__ == "__main__":
    check_template_status()
