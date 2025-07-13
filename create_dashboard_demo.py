#!/usr/bin/env python
import os
import sys
import django

# הגדרות Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, Customer, Bike, User, RepairCategory, RepairSubCategory
from django.contrib.auth.models import Group
from django.utils import timezone

print("🧪 יוצר נתוני דמו לדשבורד מנהל...")

# יצירת לקוח דמו אם לא קיים
try:
    customer = Customer.objects.get(name="דמו לדשבורד")
except Customer.DoesNotExist:
    # יצירת משתמש ללקוח
    try:
        demo_user = User.objects.get(username="demo_customer")
    except User.DoesNotExist:
        demo_user = User.objects.create_user(
            username="demo_customer",
            password="1234",
            first_name="לקוח",
            last_name="דמו"
        )
        # הוספה לקבוצת לקוחות
        customers_group, _ = Group.objects.get_or_create(name='Customers')
        demo_user.groups.add(customers_group)
    
    customer = Customer.objects.create(
        name="דמו לדשבורד",
        phone="050-1234567",
        email="demo@example.com",
        user=demo_user
    )
    print(f"✅ לקוח נוצר: {customer.name}")

# יצירת אופניים אם לא קיימות
try:
    bike = Bike.objects.get(customer=customer, brand="דמו")
except Bike.DoesNotExist:
    bike = Bike.objects.create(
        customer=customer,
        brand="דמו",
        model="טסט",
        color="כחול"
    )
    print(f"✅ אופניים נוצרו: {bike}")

# מציאת מכונאי אם קיים
try:
    mechanic = User.objects.filter(groups__name='Mechanics').first()
    if not mechanic:
        print("⚠️ לא נמצא מכונאי במערכת")
        mechanic = None
except:
    mechanic = None

# יצירת תיקונים בסטטוסים שונים
statuses_to_create = [
    ('reported', 'דווח על ידי לקוח'),
    ('diagnosed', 'מאובחן - ממתין לאישור'),
    ('partially_approved', 'אושר חלקית'),
    ('approved', 'אושר - ממתין להתחלה'),
    ('in_progress', 'בביצוע'),
]

for status_code, status_name in statuses_to_create:
    # בדיקה אם כבר קיים תיקון עם הסטטוס הזה
    existing = RepairJob.objects.filter(status=status_code).first()
    if not existing:
        repair = RepairJob.objects.create(
            bike=bike,
            problem_description=f"בעיה לדמו - {status_name}",
            status=status_code,
            assigned_mechanic=mechanic if status_code in ['approved', 'in_progress'] else None,
        )
        print(f"✅ תיקון נוצר: סטטוס {status_code}")
    else:
        print(f"⚠️ תיקון עם סטטוס {status_code} כבר קיים")

# יצירת תיקון תקוע
stuck_repair = RepairJob.objects.filter(is_stuck=True).first()
if not stuck_repair:
    repair = RepairJob.objects.create(
        bike=bike,
        problem_description="בעיה תקועה לדמו",
        status='in_progress',
        assigned_mechanic=mechanic,
        is_stuck=True,
        stuck_reason="חסר חלק במחסן",
        stuck_at=timezone.now()
    )
    print(f"✅ תיקון תקוע נוצר")
else:
    print(f"⚠️ תיקון תקוע כבר קיים")

print("\n📊 סיכום נתונים:")
print(f"תיקונים דווחו: {RepairJob.objects.filter(status='reported').count()}")
print(f"תיקונים מאובחנים: {RepairJob.objects.filter(status='diagnosed').count()}")
print(f"תיקונים מאושרים חלקית: {RepairJob.objects.filter(status='partially_approved').count()}")
print(f"תיקונים מאושרים: {RepairJob.objects.filter(status='approved').count()}")
print(f"תיקונים בביצוע: {RepairJob.objects.filter(status='in_progress').count()}")
print(f"תיקונים תקועים: {RepairJob.objects.filter(is_stuck=True).count()}")

print("\n🎉 נתוני דמו נוצרו! עכשיו הדשבורד אמור להציג נתונים.")
