from workshop.models import Customer, Bike, RepairJob, RepairItem
from django.contrib.auth.models import User
from django.utils import timezone

customer, created = Customer.objects.get_or_create(
    name="Test Customer Button",
    defaults={'phone': '050-1234567', 'email': 'test@test.com'}
)

bike, created = Bike.objects.get_or_create(
    customer=customer,
    brand="Trek",
    model="Test Bike",
    defaults={'color': 'Red'}
)

mechanic, created = User.objects.get_or_create(
    username="mechanic_test_button",
    defaults={'first_name': 'Yossi', 'last_name': 'Mechanic', 'email': 'mech@test.com'}
)

repair = RepairJob.objects.create(
    bike=bike,
    assigned_mechanic=mechanic,
    problem_description='Test button issue - wheel problem',
    status='in_progress',
    is_stuck=True,
    stuck_reason='Missing part - rear wheel, need to order from supplier',
    stuck_at=timezone.now(),
    diagnosed_at=timezone.now()
)

RepairItem.objects.create(
    repair_job=repair,
    description='Replace rear wheel 26 inch',
    price=150,
    is_approved_by_customer=True,
    status='blocked',
    notes='Missing in stock - need to order from supplier'
)

RepairItem.objects.create(
    repair_job=repair,
    description='Adjust rear brakes',
    price=50,
    is_approved_by_customer=True,
    status='pending'
)

print(f"Created stuck repair #{repair.id} for testing respond button")
print(f"Mechanic: {mechanic.get_full_name()}")
print(f"Stuck reason: {repair.stuck_reason}")
print("Now go to manager dashboard and test the 'Respond' button")
