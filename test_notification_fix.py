#!/usr/bin/env python3
"""
בדיקת התיקון לשגיאת message_map
"""

import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_notification_function():
    """בדיקת הפונקציה send_customer_notification"""
    from workshop.models import RepairJob, Customer, Bike
    from workshop.views import send_customer_notification
    from django.contrib.auth.models import User
    
    print("🧪 בדיקת פונקציית ההתראות...")
    
    # נמצא תיקון קיים לבדיקה
    repair_jobs = RepairJob.objects.all()
    if not repair_jobs.exists():
        print("❌ אין תיקונים במערכת לבדיקה")
        return False
        
    repair_job = repair_jobs.first()
    print(f"✅ נמצא תיקון לבדיקה: {repair_job}")
    
    # נמצא משתמש לבדיקה
    users = User.objects.filter(is_staff=True)
    if not users.exists():
        print("❌ אין משתמשים לבדיקה")
        return False
        
    user = users.first()
    print(f"✅ נמצא משתמש לבדיקה: {user}")
    
    try:
        # בדיקה עם לקוח עם אימייל
        print("\n📧 בדיקה עם לקוח עם אימייל...")
        customer = repair_job.bike.customer
        if not customer.email:
            customer.email = "test@example.com"
            customer.save()
        
        send_customer_notification(
            repair_job=repair_job,
            message_type='diagnosis_ready',
            extra_message="בדיקה אוטומטית",
            user=user
        )
        print("✅ הפונקציה עבדה עם לקוח עם אימייל")
        
        # בדיקה עם לקוח ללא אימייל
        print("\n📭 בדיקה עם לקוח ללא אימייל...")
        customer.email = ""
        customer.save()
        
        send_customer_notification(
            repair_job=repair_job,
            message_type='diagnosis_ready',
            extra_message="בדיקה אוטומטית ללא אימייל",
            user=user
        )
        print("✅ הפונקציה עבדה עם לקוח ללא אימייל")
        
        # בדיקה עם message_type לא קיים
        print("\n❓ בדיקה עם message_type לא קיים...")
        send_customer_notification(
            repair_job=repair_job,
            message_type='unknown_type',
            extra_message="הודעה עם סוג לא ידוע",
            user=user
        )
        print("✅ הפונקציה עבדה עם message_type לא קיים")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקה: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔧 בדיקת תיקון שגיאת message_map")
    print("=" * 40)
    
    if test_notification_function():
        print("\n🎉 כל הבדיקות עברו בהצלחה!")
        print("\n📋 מה תוקן:")
        print("1. הוצאת message_map מבלוק ה-if")
        print("2. הוספת בדיקת null-safety לחיתוך ההודעה")
        print("3. הפונקציה עובדת גם כשאין אימייל ללקוח")
        print("\n✨ השגיאה אמורה להיפתר עכשיו!")
    else:
        print("\n💥 עדיין יש בעיות שצריך לפתור")

if __name__ == "__main__":
    main()
