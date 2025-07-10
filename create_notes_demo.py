#!/usr/bin/env python3
"""
דמו לבדיקת פונקציונליות הערות המכונאי
"""

import os
import sys
import django

# הגדרת נתיב Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import Customer, Bike, RepairJob, RepairItem, UserProfile

def create_test_data():
    """יצירת נתוני דמו לבדיקת ההערות"""
    
    print("🔧 יוצר נתוני דמו להערות מכונאי...")
    
    # יצירת מכונאי
    mechanic_user, created = User.objects.get_or_create(
        username='mechanic_demo',
        defaults={
            'first_name': 'יוסי',
            'last_name': 'המכונאי',
            'email': 'mechanic@demo.com'
        }
    )
    if created:
        mechanic_user.set_password('demo123')
        mechanic_user.save()
    
    mechanic_profile, _ = UserProfile.objects.get_or_create(
        user=mechanic_user,
        defaults={'role': 'mechanic'}
    )
    
    # יצירת לקוח
    customer, _ = Customer.objects.get_or_create(
        name='דוד כהן - דמו',
        defaults={
            'phone': '054-1234567',
            'email': 'david@demo.com'
        }
    )
    
    # יצירת אופניים
    bike, _ = Bike.objects.get_or_create(
        customer=customer,
        brand='Trek',
        defaults={
            'model': 'Mountain X3',
            'color': 'שחור'
        }
    )
    
    # יצירת תיקון
    repair_job, created = RepairJob.objects.get_or_create(
        bike=bike,
        defaults={
            'problem_description': 'הילוכים לא פועלים, בלמים צורמים',
            'diagnosis': 'נדרש כוונון הילוכים והחלפת רפידות בלמים',
            'status': 'in_progress',
            'assigned_mechanic': mechanic_user
        }
    )
    
    if created:
        # יצירת פעולות תיקון דמו
        items_data = [
            {
                'description': 'כוונון מערכת הילוכים',
                'price': 120.00,
                'is_approved_by_customer': True,
                'notes': 'התגלתה בעיה נוספת - כבל הילוכים פגום, נדרש החלפה'
            },
            {
                'description': 'החלפת רפידות בלמים קדמיים',
                'price': 80.00,
                'is_approved_by_customer': True,
                'is_completed': True,
                'completed_by': mechanic_user,
                'notes': 'הושלם בהצלחה. רפידות איכותיות הותקנו.'
            },
            {
                'description': 'החלפת כבל הילוכים',
                'price': 45.00,
                'is_approved_by_customer': True,
                'notes': 'חסר כבל במלאי, הוזמן מהספק. יגיע ביום רביעי.'
            },
            {
                'description': 'שמן שרשרת וכללי',
                'price': 25.00,
                'is_approved_by_customer': True,
                'is_completed': True,
                'completed_by': mechanic_user,
                'notes': 'הושלם. שרשרת הייתה מאוד מלוכלכת - מומלץ ללקוח על ניקוי קבוע.'
            }
        ]
        
        for item_data in items_data:
            RepairItem.objects.create(
                repair_job=repair_job,
                **item_data
            )
    
    print(f"✅ נוצר תיקון דמו #{repair_job.id}")
    print(f"📝 מכונאי: {mechanic_user.get_full_name()} (username: {mechanic_user.username})")
    print(f"🚲 אופניים: {bike}")
    print(f"👤 לקוח: {customer.name}")
    print("\n🎯 כעת ניתן לבדוק:")
    print("1. התחבר כמכונאי וראה את הטופס עם שדות ההערות")
    print("2. התחבר כמנהל וראה את ההערות בדף סטטוס התיקון")
    print(f"\n🌐 כתובת: http://127.0.0.1:8000/workshop/repair/{repair_job.id}/status/")
    
    return repair_job

if __name__ == '__main__':
    create_test_data()
