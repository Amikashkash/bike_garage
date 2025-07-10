#!/usr/bin/env python3
"""
בדיקה מהירה של התיקון
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob
from workshop.views import send_customer_notification
from django.contrib.auth.models import User

# בדיקה מהירה
try:
    repair_job = RepairJob.objects.first()
    user = User.objects.filter(is_staff=True).first()
    
    if repair_job and user:
        # ווידוא שללקוח אין אימייל כדי לבדוק את המקרה הבעייתי
        customer = repair_job.bike.customer
        customer.email = ""
        customer.save()
        
        # קריאה לפונקציה - זה המקרה שגרם לשגיאה
        send_customer_notification(
            repair_job=repair_job,
            message_type='diagnosis_ready',
            extra_message="בדיקה",
            user=user
        )
        print("✅ הפונקציה עבדה ללא שגיאות!")
    else:
        print("❌ לא נמצאו נתונים לבדיקה")
        
except Exception as e:
    print(f"❌ שגיאה: {e}")
    import traceback
    traceback.print_exc()
