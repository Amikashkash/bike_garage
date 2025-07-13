#!/usr/bin/env python
import os
import sys
import django

# הגדרות Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob

print("=== בדיקת סטטוס תיקונים ===")

# בדיקת סטטוסים
for status_code, status_name in RepairJob.STATUS_CHOICES:
    count = RepairJob.objects.filter(status=status_code).count()
    print(f'{status_code}: {count} repairs')

print("\n=== תיקונים תקועים ===")
stuck_count = RepairJob.objects.filter(is_stuck=True).count()
print(f'Stuck repairs: {stuck_count}')

print("\n=== כל התיקונים ===")
all_repairs = RepairJob.objects.all()
print(f'Total repairs: {all_repairs.count()}')

for repair in all_repairs[:10]:
    print(f'Repair #{repair.id}: {repair.bike} - Status: {repair.status} - Stuck: {repair.is_stuck} - Assigned: {repair.assigned_mechanic}')

print("\n=== בדיקת שדות ===")
if all_repairs.exists():
    first_repair = all_repairs.first()
    print(f'First repair fields:')
    print(f'  - has is_stuck field: {hasattr(first_repair, "is_stuck")}')
    print(f'  - has status field: {hasattr(first_repair, "status")}')
    print(f'  - has assigned_mechanic field: {hasattr(first_repair, "assigned_mechanic")}')
