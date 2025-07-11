from workshop.models import RepairJob, RepairItem

# בדיקת תיקון #10
try:
    repair = RepairJob.objects.get(id=10)
    print(f"תיקון #{repair.id}:")
    print(f"  מכונאי: {repair.assigned_mechanic}")
    print(f"  is_stuck: {getattr(repair, 'is_stuck', 'לא קיים')}")
    print(f"  stuck_reason: {getattr(repair, 'stuck_reason', 'לא קיים')}")
    print(f"  סטטוס כללי: {repair.status}")
    print()
    
    print("פריטים:")
    approved_items = repair.repair_items.filter(is_approved_by_customer=True)
    completed_count = 0
    blocked_count = 0
    
    for item in approved_items:
        print(f"  {item.description}: status={item.status}, is_completed={item.is_completed}")
        if item.status == 'completed':
            completed_count += 1
        elif item.status == 'blocked':
            blocked_count += 1
    
    total_approved = approved_items.count()
    progress = (completed_count / total_approved * 100) if total_approved > 0 else 0
    
    print(f"\nסיכום:")
    print(f"  סה\"כ פריטים מאושרים: {total_approved}")
    print(f"  הושלמו: {completed_count}")
    print(f"  תקועים: {blocked_count}")
    print(f"  אחוז התקדמות: {progress:.1f}%")
    
    # לוגיקת הקטגוריזציה
    is_repair_stuck = getattr(repair, 'is_stuck', False)
    print(f"\nקטגוריזציה:")
    print(f"  תיקון כולו תקוע (is_stuck): {is_repair_stuck}")
    print(f"  יש פריטים תקועים: {blocked_count > 0}")
    
    if is_repair_stuck:
        print("  -> אמור להופיע ב: משימות תקועות")
    elif progress == 0:
        print("  -> אמור להופיע ב: משימות ממתינות להתחלה")
    elif 0 < progress < 100:
        print("  -> אמור להופיע ב: משימות בביצוע פעיל")
    else:
        print("  -> הושלם")

except RepairJob.DoesNotExist:
    print("תיקון #10 לא נמצא")
