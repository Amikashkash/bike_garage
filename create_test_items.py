#!/usr/bin/env python3
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem
from django.contrib.auth.models import User

# מציאת תיקון קיים
try:
    job = RepairJob.objects.get(id=9)
    print(f'נמצא תיקון: {job}')
    
    # מחיקת פריטים קיימים
    job.repair_items.all().delete()
    
    # יצירת פריטי תיקון חדשים עם הערות
    items = [
        {
            'description': 'כוונון הילוכים',
            'price': 120.00,
            'is_approved_by_customer': True,
            'notes': 'התגלתה בעיה נוספת - כבל הילוכים פגום ונדרש החלפה. הוזמן חלק חדש מהספק.'
        },
        {
            'description': 'החלפת רפידות בלמים',
            'price': 80.00,
            'is_approved_by_customer': True,
            'is_completed': True,
            'notes': 'הושלם בהצלחה. רפידות איכותיות הותקנו. מומלץ בדיקה לאחר 100 ק"מ.'
        },
        {
            'description': 'ניקוי ושמן שרשרת',
            'price': 25.00,
            'is_approved_by_customer': True,
            'is_completed': True,
            'notes': 'השרשרת הייתה מאוד מלוכלכת. בוצע ניקוי יסודי. מומלץ ללקוח על תחזוקה קבועה.'
        }
    ]
    
    # מציאת מכונאי
    try:
        mechanic = User.objects.get(username='mechanic_demo')
    except:
        mechanic = None
    
    for item_data in items:
        item = RepairItem.objects.create(
            repair_job=job,
            description=item_data['description'],
            price=item_data['price'],
            is_approved_by_customer=item_data['is_approved_by_customer'],
            is_completed=item_data.get('is_completed', False),
            notes=item_data['notes'],
            completed_by=mechanic if item_data.get('is_completed') else None
        )
        print(f'נוצר פריט: {item.description}')
    
    print(f'\n✅ נוצרו {len(items)} פריטי תיקון עם הערות')
    print(f'🔗 בדוק בכתובת: http://127.0.0.1:8000/workshop/repair/{job.id}/status/')
    
except RepairJob.DoesNotExist:
    print('❌ תיקון #9 לא נמצא')
    print('תיקונים זמינים:')
    for job in RepairJob.objects.all()[:5]:
        print(f'  תיקון #{job.id}: {job.bike}')
