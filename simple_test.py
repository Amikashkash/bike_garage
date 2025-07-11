#!/usr/bin/env python
import os
import django

# הגדרת סביבת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')

# הגדרת נתיב
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

try:
    from workshop.models import RepairItem
    
    # בדיקת שדה status
    item = RepairItem.objects.first()
    if item:
        print(f"שדה status קיים: {hasattr(item, 'status')}")
        print(f"ערך status: {item.status}")
        print(f"אפשרויות status: {RepairItem.STATUS_CHOICES}")
        
        # בדיקת עדכון
        original_status = item.status
        print(f"סטטוס מקורי: {original_status}")
        
        item.status = 'blocked'
        item.save()
        print(f"סטטוס אחרי עדכון לחסום: {item.status}")
        print(f"is_completed אחרי עדכון: {item.is_completed}")
        
        item.status = 'completed'
        item.save()
        print(f"סטטוס אחרי עדכון למושלם: {item.status}")
        print(f"is_completed אחרי עדכון: {item.is_completed}")
        
        # החזרה למקורי
        item.status = original_status
        item.save()
        print(f"סטטוס הוחזר למקורי: {item.status}")
        
    else:
        print("אין פריטים במערכת")
        
except Exception as e:
    print(f"שגיאה: {e}")
