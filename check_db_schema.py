#!/usr/bin/env python3
"""
בדיקת מבנה מסד הנתונים
"""

import os
import sys
import django

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection
from workshop.models import RepairJob

def check_database_schema():
    print("=== בדיקת מבנה מסד הנתונים ===")
    
    cursor = connection.cursor()
    
    # בדיקת עמודות בטבלת RepairJob
    cursor.execute("PRAGMA table_info(workshop_repairjob)")
    columns = cursor.fetchall()
    
    print("\n=== עמודות בטבלת workshop_repairjob ===")
    stuck_fields = []
    for col in columns:
        col_name = col[1]
        col_type = col[2]
        print(f"  {col_name}: {col_type}")
        if 'stuck' in col_name:
            stuck_fields.append(col_name)
    
    print(f"\n=== שדות הקשורים לתקיעות: {stuck_fields} ===")
    
    # בדיקת נתונים קיימים
    print("\n=== בדיקת תיקונים קיימים ===")
    repairs = RepairJob.objects.all()[:5]
    
    for repair in repairs:
        print(f"תיקון {repair.id}:")
        print(f"  is_stuck: {getattr(repair, 'is_stuck', 'שדה לא קיים')}")
        print(f"  stuck_reason: {getattr(repair, 'stuck_reason', 'שדה לא קיים')}")
        print(f"  stuck_at: {getattr(repair, 'stuck_at', 'שדה לא קיים')}")
        print()

if __name__ == "__main__":
    check_database_schema()
