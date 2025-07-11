#!/usr/bin/env python3
"""
🔧 יצירת תיקון לבדיקת התיקון
"""

import os
import sys
import django

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import RepairJob, RepairItem, Customer, Bike, RepairCategory
from django.utils import timezone

def create_test_repair():
    print("=== יצירת תיקון לבדיקה ===")
    
    # מציאת מכונאי
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    if not mechanic:
        print("❌ לא נמצא מכונאי")
        return
    
    print(f"✅ נמצא מכונאי: {mechanic.username}")
    
    # מציאת לקוח או יצירת אחד חדש
    customer = Customer.objects.first()
    if not customer:
        customer = Customer.objects.create(
            name="לקוח בדיקה",
            phone="050-1234567",
            email="test@example.com"
        )
        print("✅ נוצר לקוח חדש")
    else:
        print(f"✅ נמצא לקוח: {customer.name}")
    
    # יצירת אופניים
    bike, created = Bike.objects.get_or_create(
        customer=customer,
        brand="Trek",
        model="Mountain Bike",
        defaults={
            'color': 'כחול'
        }
    )
    if created:
        print("✅ נוצרו אופניים חדשות")
    else:
        print(f"✅ נמצאו אופניים: {bike}")
    
    # יצירת תיקון
    repair_job = RepairJob.objects.create(
        bike=bike,
        problem_description="בדיקת המערכת החדשה",
        diagnosis="צריך החלפת בלמים ושרשרת",
        status='in_progress',
        assigned_mechanic=mechanic,
        created_at=timezone.now()
    )
    print(f"✅ נוצר תיקון: #{repair_job.id}")
    
    # יצירת פעולות תיקון
    items_data = [
        {"description": "החלפת בלמים קדמיים", "price": 150.00},
        {"description": "החלפת בלמים אחוריים", "price": 150.00},
        {"description": "החלפת שרשרת", "price": 80.00},
        {"description": "כיוונון הילוכים", "price": 50.00},
    ]
    
    for item_data in items_data:
        item = RepairItem.objects.create(
            repair_job=repair_job,
            description=item_data["description"],
            price=item_data["price"],
            is_approved_by_customer=True,  # מאושר מראש לבדיקה
        )
        print(f"   ✅ נוצרה פעולה: {item.description}")
    
    print(f"\n🎯 תיקון מוכן לבדיקה!")
    print(f"   🌐 URL למכונאי: http://localhost:8000/mechanic/task-completion/{repair_job.id}/")
    print(f"   👤 התחבר כ: {mechanic.username}")
    
    return repair_job

if __name__ == "__main__":
    create_test_repair()
