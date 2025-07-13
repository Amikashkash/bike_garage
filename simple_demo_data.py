#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob

# בדיקה פשוטה של הנתונים
repairs = RepairJob.objects.all()
print(f"Total repairs: {repairs.count()}")

for repair in repairs:
    print(f"Repair #{repair.id} - Status: {repair.status} - Stuck: {getattr(repair, 'is_stuck', 'NO FIELD')}")

print("Creating demo data...")

# יצירת נתוני דמו פשוט
from django.contrib.auth.models import User
from workshop.models import Customer, Bike

# מציאת או יצירת לקוח
customer, created = Customer.objects.get_or_create(
    name="Test Customer",
    defaults={
        'phone': '050-1234567',
        'email': 'test@test.com'
    }
)

# מציאת או יצירת אופניים
bike, created = Bike.objects.get_or_create(
    customer=customer,
    brand="Test",
    defaults={
        'model': 'Model',
        'color': 'Blue'
    }
)

# יצירת תיקונים
statuses = ['reported', 'diagnosed', 'approved', 'in_progress']
for status in statuses:
    repair, created = RepairJob.objects.get_or_create(
        bike=bike,
        status=status,
        defaults={
            'problem_description': f'Test problem for {status}',
        }
    )
    if created:
        print(f"Created repair with status: {status}")

print("Done!")
