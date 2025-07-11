from workshop.models import RepairJob, RepairItem

# בדיקת השדה החדש status
jobs = RepairJob.objects.all()[:3]
print(f"נמצאו {jobs.count()} תיקונים")

if jobs:
    for job in jobs:
        print(f"תיקון #{job.id} - {job.bike}")
        items = job.repair_items.all()
        for item in items:
            print(f"  פעולה: {item.description}")
            print(f"  סטטוס: {item.status}")
            print(f"  is_completed: {item.is_completed}")
            print("---")
else:
    print("אין תיקונים במערכת")

# בדיקת עדכון סטטוס
if jobs:
    first_job = jobs.first()
    items = first_job.repair_items.all()
    if items:
        test_item = items.first()
        print(f"\nבדיקת עדכון סטטוס עבור: {test_item.description}")
        
        # עדכון לתקוע
        test_item.status = 'blocked'
        test_item.notes = "בדיקת מערכת"
        test_item.save()
        
        test_item.refresh_from_db()
        print(f"סטטוס אחרי עדכון לתקוע: {test_item.status}")
        print(f"is_completed: {test_item.is_completed}")
        
        # עדכון להושלם
        test_item.status = 'completed'
        test_item.save()
        
        test_item.refresh_from_db()
        print(f"סטטוס אחרי עדכון להושלם: {test_item.status}")
        print(f"is_completed: {test_item.is_completed}")
