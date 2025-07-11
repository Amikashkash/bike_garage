from workshop.models import Customer, Bike, RepairJob, RepairItem
from django.contrib.auth.models import User
from django.utils import timezone

# יצירת לקוח לבדיקה
customer, created = Customer.objects.get_or_create(
    name="בדיקת כפתור השב",
    defaults={'phone': '050-1234567', 'email': 'test@test.com'}
)

# יצירת אופניים
bike, created = Bike.objects.get_or_create(
    customer=customer,
    brand="Trek",
    model="Test Bike",
    defaults={'color': 'אדום'}
)

# יצירת מכונאי
mechanic, created = User.objects.get_or_create(
    username="mechanic_button_test",
    defaults={'first_name': 'יוסי', 'last_name': 'בדיקה', 'email': 'mech@test.com'}
)

# יצירת תיקון תקוע
repair = RepairJob.objects.create(
    bike=bike,
    assigned_mechanic=mechanic,
    problem_description='בדיקת כפתור השב - בעיה בגלגלים',
    status='in_progress',
    is_stuck=True,
    stuck_reason='חסר חלק חילוף - גלגל אחורי, צריך להזמין מהספק',
    stuck_at=timezone.now(),
    diagnosed_at=timezone.now()
)

# יצירת פעולות תיקון
RepairItem.objects.create(
    repair_job=repair,
    description='החלפת גלגל אחורי 26 אינץ',
    price=150,
    is_approved_by_customer=True,
    status='blocked',
    notes='חסר במחסן - צריך להזמין מהספק'
)

RepairItem.objects.create(
    repair_job=repair,
    description='כוונון בלמים אחורים',
    price=50,
    is_approved_by_customer=True,
    status='pending'
)

print(f"נוצר תיקון תקוע #{repair.id} לבדיקת כפתור השב")
print(f"מכונאי: {mechanic.get_full_name()}")
print(f"סיבת תקיעות: {repair.stuck_reason}")
print("כעת גש לדשבורד המנהל ובדוק את כפתור 'השב'")
