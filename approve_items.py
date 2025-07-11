#!/usr/bin/env python3
import os, sys, django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem

repair = RepairJob.objects.get(id=12)
items = repair.repair_items.all()
for item in items:
    item.is_approved_by_customer = True
    item.save()
    print(f'אישרנו: {item.description}')
print(f'סה״כ פעולות מאושרות: {repair.repair_items.filter(is_approved_by_customer=True).count()}')
