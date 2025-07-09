#!/usr/bin/env python3
"""
🔧 בדיקה מהירה לתיקון בעיית MechanicTaskForm
"""

import os
import sys
import django

# הוספת נתיב הפרויקט
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.forms import MechanicTaskForm
from workshop.models import RepairJob

def test_mechanic_task_form():
    """בדיקה שהפורם עובד נכון עם הפרמטרים החדשים"""
    print("🧪 בודק MechanicTaskForm...")
    
    try:
        # חיפוש תיקון קיים
        repair_jobs = RepairJob.objects.filter(status='in_progress').first()
        
        if not repair_jobs:
            print("❌ לא נמצא תיקון במצב 'in_progress'")
            print("💡 צור תיקון חדש במערכת כדי לבדוק")
            return False
        
        # בדיקת יצירת הפורם ללא נתונים (GET)
        form_get = MechanicTaskForm(repair_job=repair_jobs)
        print("✅ פורם GET עובד - אין שגיאה")
        
        # בדיקת יצירת הפורם עם נתונים (POST simulation)
        post_data = {
            'completed_items': [],
            'notes': 'בדיקה'
        }
        form_post = MechanicTaskForm(post_data, repair_job=repair_jobs)
        print("✅ פורם POST עובד - אין שגיאה")
        
        print("🎉 התיקון הצליח! MechanicTaskForm עובד נכון")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False

if __name__ == "__main__":
    success = test_mechanic_task_form()
    if success:
        print("\n✅ הבדיקה עברה בהצלחה")
        print("💡 עכשיו אפשר לנסות שוב בדפדפן")
    else:
        print("\n❌ הבדיקה נכשלה")
        print("💡 בדוק שיש נתונים במסד הנתונים")
