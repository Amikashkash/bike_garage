#!/usr/bin/env python3
"""
דמו למערכת סימון תיקונים תקועים
"""

import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, Bike, Customer, WorkshopUser
from django.contrib.auth.models import User
from django.utils import timezone

def create_stuck_repair_demo():
    """יוצר דמו של תיקון תקוע"""
    
    print("🔧 יוצר דמו למערכת תיקונים תקועים...")
    
    # יצירת משתמש מנהל
    manager_user, created = User.objects.get_or_create(
        username='manager1',
        defaults={
            'first_name': 'אבי',
            'last_name': 'המנהל',
            'email': 'manager@bikegarage.com'
        }
    )
    if created:
        manager_user.set_password('123')
        manager_user.save()
    
    manager_profile, created = WorkshopUser.objects.get_or_create(
        user=manager_user,
        defaults={'role': 'manager'}
    )
    
    # יצירת מכונאי
    mechanic_user, created = User.objects.get_or_create(
        username='mechanic_stuck',
        defaults={
            'first_name': 'יוסי',
            'last_name': 'המכונאי'
        }
    )
    if created:
        mechanic_user.set_password('123')
        mechanic_user.save()
    
    mechanic_profile, created = WorkshopUser.objects.get_or_create(
        user=mechanic_user,
        defaults={'role': 'mechanic'}
    )
    
    # יצירת לקוח
    customer_user, created = User.objects.get_or_create(
        username='customer_stuck',
        defaults={
            'first_name': 'דני',
            'last_name': 'הלקוח'
        }
    )
    if created:
        customer_user.set_password('123')
        customer_user.save()
    
    customer, created = Customer.objects.get_or_create(
        user=customer_user,
        defaults={
            'name': 'דני הלקוח',
            'phone': '052-9876543',
            'email': 'customer@test.com'
        }
    )
    
    # יצירת אופניים
    bike, created = Bike.objects.get_or_create(
        customer=customer,
        brand='Specialized',
        defaults={
            'model': 'Rockhopper',
            'year': 2021,
            'color': 'אדום'
        }
    )
    
    # יצירת תיקון תקוע
    repair_job, created = RepairJob.objects.get_or_create(
        bike=bike,
        defaults={
            'problem_description': 'בעיה חמורה בהילוכים - לא עוברים בכלל',
            'status': 'in_progress',
            'assigned_mechanic': mechanic_user,
            'diagnosis': 'נדרש החלפת מערכת הילוכים מלאה',
            'is_stuck': True,
            'stuck_reason': 'חסר חלק מסוים בדרישה מיוחדת - Shimano Deore XT 12-speed. המוצר אזל מהמחסן ואני לא בטוח איך להמשיך. בנוסף, יש בעיה עם הכלי המיוחד שנדרש לפירוק.',
            'stuck_at': timezone.now()
        }
    )
    
    if created:
        # יצירת פריטי תיקון
        RepairItem.objects.create(
            repair_job=repair_job,
            description='החלפת קלטת הילוכים אחורית',
            price=180,
            is_approved_by_customer=True,
            is_completed=False
        )
        
        RepairItem.objects.create(
            repair_job=repair_job,
            description='החלפת מחליף הילוכים',
            price=120,
            is_approved_by_customer=True,
            is_completed=False
        )
        
        RepairItem.objects.create(
            repair_job=repair_job,
            description='כיוונון מערכת הילוכים',
            price=60,
            is_approved_by_customer=True,
            is_completed=True,
            completed_by=mechanic_user,
            completed_at=timezone.now(),
            notes='הכיוונון הבסיסי בוצע, אבל חסר החלק העיקרי'
        )
    
    print("✅ דמו נוצר בהצלחה!")
    print(f"👤 מנהל: {manager_user.username} / סיסמה: 123")
    print(f"🔧 מכונאי: {mechanic_user.username} / סיסמה: 123")
    print(f"👨‍💼 לקוח: {customer_user.username} / סיסמה: 123")
    print(f"🚲 תיקון #{repair_job.id} - {bike}")
    print(f"⚠️ סטטוס: תקוע - {repair_job.stuck_reason[:50]}...")
    print()
    print("🌐 URLים לבדיקה:")
    print(f"   מנהל: http://127.0.0.1:8000/manager/dashboard/")
    print(f"   מכונאי: http://127.0.0.1:8000/mechanic/dashboard/")
    print(f"   תיקון: http://127.0.0.1:8000/repair/{repair_job.id}/")
    
    return repair_job

if __name__ == "__main__":
    create_stuck_repair_demo()
