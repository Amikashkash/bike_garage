#!/usr/bin/env python
import os
import sys
import django

# הוספת הנתיב לסביבה
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import Customer, Bike, Repair, RepairItem
from django.contrib.auth.models import User

def create_stuck_repair():
    """יצירת תיקון תקוע לבדיקת הכפתור"""
    
    # יצירת לקוח אם לא קיים
    customer, created = Customer.objects.get_or_create(
        name="לקוח בדיקה",
        defaults={
            'phone': '050-1234567',
            'email': 'test@example.com'
        }
    )
    print(f"לקוח: {customer.name} ({'נוצר חדש' if created else 'קיים'})")
    
    # יצירת אופניים אם לא קיימות
    bike, created = Bike.objects.get_or_create(
        customer=customer,
        brand="Trek",
        model="Test Bike",
        defaults={'year': 2023}
    )
    print(f"אופניים: {bike} ({'נוצרו חדשות' if created else 'קיימות'})")
    
    # יצירת מכונאי אם לא קיים
    mechanic, created = User.objects.get_or_create(
        username="mechanic_test",
        defaults={
            'first_name': 'יוסי',
            'last_name': 'מכונאי',
            'email': 'mechanic@example.com'
        }
    )
    print(f"מכונאי: {mechanic.get_full_name()} ({'נוצר חדש' if created else 'קיים'})")
    
    # יצירת תיקון
    repair, created = Repair.objects.get_or_create(
        bike=bike,
        assigned_mechanic=mechanic,
        defaults={
            'problem_description': 'בדיקת כפתור השב - בעיית גלגלים',
            'status': 'in_progress',
            'is_stuck': True,
            'stuck_reason': 'חסר חלק חילוף - גלגל אחורי 26 אינץ',
        }
    )
    
    if created:
        # סימון שהתיקון אובחן ואושר
        repair.status = 'in_progress'
        repair.diagnosed_at = django.utils.timezone.now()
        repair.customer_approved = True
        repair.is_stuck = True
        repair.stuck_reason = 'חסר חלק חילוף - גלגל אחורי 26 אינץ'
        repair.stuck_at = django.utils.timezone.now()
        repair.save()
        
        # יצירת פעולות תיקון
        item1 = RepairItem.objects.create(
            repair=repair,
            description='החלפת גלגל אחורי',
            estimated_price=150,
            is_approved=True,
            status='blocked',
            notes='חסר גלגל במחסן - צריך להזמין'
        )
        
        item2 = RepairItem.objects.create(
            repair=repair,
            description='כוונון בלמים',
            estimated_price=50,
            is_approved=True,
            status='pending'
        )
        
        print(f"תיקון נוצר: #{repair.id}")
        print(f"פעולות: {RepairItem.objects.filter(repair=repair).count()}")
        print(f"סטטוס: {repair.status}")
        print(f"תקוע: {repair.is_stuck}")
        print(f"סיבת תקיעות: {repair.stuck_reason}")
        
    else:
        print(f"תיקון קיים: #{repair.id}")
    
    return repair

if __name__ == '__main__':
    print("=== יצירת תיקון תקוע לבדיקת כפתור השב ===")
    repair = create_stuck_repair()
    print(f"\n✅ תיקון #{repair.id} מוכן לבדיקה!")
    print("גש לדשבורד המנהל: http://127.0.0.1:8000/manager/")
    print("ובדוק את כפתור 'השב' בסעיף 'תיקונים תקועים'")
