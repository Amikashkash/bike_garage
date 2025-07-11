from workshop.models import RepairJob

repair = RepairJob.objects.get(id=10)
print("Repair ID:", repair.id)
print("Mechanic:", repair.assigned_mechanic)
print("Status:", repair.status)
print("Is stuck:", getattr(repair, 'is_stuck', 'not found'))
print("Stuck reason:", getattr(repair, 'stuck_reason', 'not found'))

items = repair.repair_items.filter(is_approved_by_customer=True)
completed = items.filter(status='completed').count()
blocked = items.filter(status='blocked').count()
total = items.count()

print("Total items:", total)
print("Completed:", completed)
print("Blocked:", blocked)
print("Progress:", (completed/total*100) if total > 0 else 0)
