#!/usr/bin/env python3
"""
סקריפט יצירת נתוני דמו מהיר
"""

import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, Bike, Customer, WorkshopUser
from django.contrib.auth.models import User

def create_quick_demo():
    """יוצר דמו מהיר"""
    
    # מחיקת נתונים קיימים
    RepairJob.objects.all().delete()
    Customer.objects.all().delete()
    User.objects.filter(username__startswith='demo').delete()
    
    print("🗑️ נתונים קיימים נמחקו")
    
    # יצירת משתמש
    user = User.objects.create_user(
        username='demo_customer',
        password='123',
        first_name='יוסי',
        last_name='כהן'
    )
    
    # יצירת לקוח
    customer = Customer.objects.create(
        user=user,
        name='יוסי כהן',
        phone='052-1234567',
        email='demo@test.com'
    )
    
    # יצירת אופניים
    bike = Bike.objects.create(
        customer=customer,
        brand='Trek',
        model='X-Caliber 8',
        year=2022,
        color='כחול'
    )
    
    # יצירת מכונאי
    mechanic_user = User.objects.create_user(
        username='demo_mechanic',
        password='123',
        first_name='דני',
        last_name='המכונאי'
    )
    
    mechanic = WorkshopUser.objects.create(
        user=mechanic_user,
        role='mechanic'
    )
    
    # יצירת תיקון
    repair_job = RepairJob.objects.create(
        bike=bike,
        problem_description='בעיה בהילוכים - לא עוברים כהלכה, שרשרת קופצת',
        status='in_progress',
        assigned_mechanic=mechanic,
        diagnosis='נדרש החלפת כבל הילוכים וכיוונון מחדש'
    )
    
    # יצירת פריטי תיקון
    items = [
        {
            'description': 'החלפת כבל הילוכים אחורי',
            'price': 80,
            'approved': True,
            'completed': True,
            'notes': 'הכבל היה שחוק מאוד. הוחלף בכבל איכותי מסוג Shimano. הבדיקה הראתה שיפור משמעותי בתפקוד ההילוכים.'
        },
        {
            'description': 'כיוונון מערכת הילוכים',
            'price': 50,
            'approved': True,
            'completed': True,
            'notes': 'בוצע כיוונון מדויק של כל ההילוכים. נבדקו כל המעברים והושגה רמת דיוק גבוהה. במהלך הכיוונון זוהו כמה בעיות קלות בשרשרת שתוקנו גם כן.'
        },
        {
            'description': 'בדיקת מערכת בלמים',
            'price': 30,
            'approved': True,
            'completed': False,
            'notes': '''זוהתה בעיה בלוחיות הבלם האחוריות!

בעיות שזוהו:
- לוחיות בלויות מעבר למותר
- רעש חריקה חזק  
- ביצועי בלימה ירודים

המלצה: החלפה מיידית נדרשת לפני רכיבה נוספת מטעמי בטיחות!'''
        },
        {
            'description': 'החלפת לוחיות בלם אחוריות',
            'price': 120,
            'approved': False,
            'completed': False,
            'notes': 'לוחיות הבלם בלויות מעבר למותר. החלפה דחופה נדרשת לפני רכיבה נוספת.'
        },
        {
            'description': 'שמן וניקוי שרשרת',
            'price': 25,
            'approved': True,
            'completed': True,
            'notes': 'שרשרת נוקתה בקפידה ושומנה בשמן איכותי. מומלץ על שמון חוזר כל 200 ק"מ.'
        }
    ]
    
    for item_data in items:
        item = RepairItem.objects.create(
            repair_job=repair_job,
            description=item_data['description'],
            price=item_data['price'],
            is_approved_by_customer=item_data['approved'],
            is_completed=item_data['completed'],
            notes=item_data['notes']
        )
        
        if item_data['completed']:
            item.completed_by = mechanic
            item.save()
    
    print(f"✅ נוצר דמו מהיר - תיקון #{repair_job.id}")
    print(f"🔧 מכונאי: {mechanic.user.get_full_name()}")
    print(f"🚲 אופניים: {bike}")
    print(f"👤 לקוח: {customer.name}")
    print(f"📋 {len(items)} פריטי תיקון")
    print(f"🌐 URL: http://127.0.0.1:8000/repair/{repair_job.id}/")
    
    return repair_job

if __name__ == "__main__":
    repair_job = create_quick_demo()
