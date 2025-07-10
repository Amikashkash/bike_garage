#!/usr/bin/env python3
"""
סקריפט פשוט ליצירת דמו ובדיקת repair_status
"""

import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, Bike, Customer, WorkshopUser
from django.contrib.auth.models import User

print("🔧 יוצר דמו פשוט...")

# בדיקה אם יש תיקון
repair_job = RepairJob.objects.first()
if repair_job:
    print(f"✅ נמצא תיקון #{repair_job.id}")
    
    # הוספת הערות לפריטים קיימים
    items = repair_job.repair_items.all()
    notes_examples = [
        "הערה קצרה לבדיקה",
        "הערה ארוכה יותר שמסבירה בפירוט מה קרה במהלך התיקון ומה צריך לדעת לגבי החלק הזה של העבודה",
        "הערה בינונית עם מספר שורות\nולפעמים גם מעברי שורה\nכדי לבדוק איך זה נראה",
        "עוד הערה לבדיקה",
        "הערה אחרונה"
    ]
    
    for i, item in enumerate(items):
        if i < len(notes_examples):
            item.notes = notes_examples[i]
            item.save()
            print(f"  💬 הוספה הערה לפריט: {item.description}")
    
    print(f"🌐 בדוק בדפדפן: http://127.0.0.1:8000/repair/{repair_job.id}/")
else:
    print("❌ לא נמצא תיקון. יוצר דמו חדש...")
    
    # יצירת דמו חדש
    try:
        user = User.objects.create_user(username='demo_user', password='123')
        customer = Customer.objects.create(user=user, name='לקוח דמו', phone='050-1234567')
        bike = Bike.objects.create(customer=customer, brand='Giant', model='Escape', year=2023)
        
        repair_job = RepairJob.objects.create(
            bike=bike,
            problem_description='בעיה בבלמים',
            status='in_progress'
        )
        
        RepairItem.objects.create(
            repair_job=repair_job,
            description='בדיקת בלמים',
            price=50,
            is_approved_by_customer=True,
            notes='בלמים נבדקו ונמצאו תקינים'
        )
        
        RepairItem.objects.create(
            repair_job=repair_job,
            description='החלפת נוזל בלמים',
            price=80,
            is_approved_by_customer=True,
            notes='נוזל בלמים הוחלף בנוזל איכותי. מומלץ על החלפה כל שנה לביצועים אופטימליים ובטיחות מקסימלית'
        )
        
        print(f"✅ נוצר דמו חדש - תיקון #{repair_job.id}")
        print(f"🌐 בדוק בדפדפן: http://127.0.0.1:8000/repair/{repair_job.id}/")
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת דמו: {e}")

print("✅ סיום!")
