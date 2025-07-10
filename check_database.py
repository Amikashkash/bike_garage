#!/usr/bin/env python3
"""
בדיקת מסד נתונים ושדות חדשים
"""

import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob
from django.db import connection

def check_database():
    """בדיקת מסד הנתונים והשדות החדשים"""
    print("🔍 בדיקת מסד הנתונים...")
    
    # בדיקת שדות בטבלה
    try:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(workshop_repairjob);")
            columns = cursor.fetchall()
            
            print("📋 עמודות בטבלת RepairJob:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # בדיקה אם השדות החדשים קיימים
            column_names = [col[1] for col in columns]
            required_fields = ['is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response']
            
            print("\n🔧 בדיקת שדות חדשים:")
            missing_fields = []
            for field in required_fields:
                if field in column_names:
                    print(f"  ✅ {field} - קיים")
                else:
                    print(f"  ❌ {field} - חסר")
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"\n⚠️  שדות חסרים: {missing_fields}")
                print("נוסיף את השדות החסרים...")
                
                field_definitions = {
                    'is_stuck': 'ALTER TABLE workshop_repairjob ADD COLUMN is_stuck BOOLEAN DEFAULT 0',
                    'stuck_reason': 'ALTER TABLE workshop_repairjob ADD COLUMN stuck_reason TEXT DEFAULT ""',
                    'stuck_at': 'ALTER TABLE workshop_repairjob ADD COLUMN stuck_at DATETIME NULL',
                    'stuck_resolved': 'ALTER TABLE workshop_repairjob ADD COLUMN stuck_resolved BOOLEAN DEFAULT 0',
                    'manager_response': 'ALTER TABLE workshop_repairjob ADD COLUMN manager_response TEXT DEFAULT ""'
                }
                
                for field in missing_fields:
                    try:
                        cursor.execute(field_definitions[field])
                        print(f"  ✅ הוסף {field}")
                    except Exception as e:
                        print(f"  ❌ שגיאה בהוספת {field}: {e}")
                
                connection.commit()
                print("✅ כל השדות נוספו!")
            else:
                print("✅ כל השדות הנדרשים קיימים!")
                
    except Exception as e:
        print(f"❌ שגיאה: {e}")
    
    # בדיקת המודל
    try:
        print("\n🧪 בדיקת המודל...")
        repairs = RepairJob.objects.all()[:1]
        if repairs:
            repair = repairs[0]
            print(f"  - תיקון #{repair.id}")
            print(f"  - is_stuck: {getattr(repair, 'is_stuck', 'לא קיים')}")
            print(f"  - stuck_reason: {getattr(repair, 'stuck_reason', 'לא קיים')}")
        else:
            print("  אין תיקונים במערכת")
            
    except Exception as e:
        print(f"❌ שגיאה במודל: {e}")

if __name__ == "__main__":
    check_database()
