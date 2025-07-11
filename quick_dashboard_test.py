from workshop.models import RepairJob, RepairItem

# בדיקה מהירה של דשבורד מנהל
in_progress = RepairJob.objects.filter(status__in=['approved', 'in_progress'])
print(f"תיקונים בביצוע: {in_progress.count()}")

if in_progress.count() > 0:
    for repair in in_progress[:3]:  # רק 3 הראשונים
        approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        completed_items = approved_items.filter(status='completed')
        blocked_items = approved_items.filter(status='blocked')
        
        progress = (completed_items.count() / approved_items.count() * 100) if approved_items.count() > 0 else 0
        is_stuck = getattr(repair, 'is_stuck', False)
        
        print(f"תיקון #{repair.id}: {progress:.1f}% הושלם, תקוע: {is_stuck}")
        
        # קטגוריה
        if is_stuck:
            category = "תקוע"
        elif progress == 0:
            category = "ממתין להתחלה"
        elif 0 < progress < 100:
            category = "בעבודה פעילה"
        else:
            category = "הושלם"
        
        print(f"   קטגוריה: {category}")

print("בדיקה הושלמה!")
