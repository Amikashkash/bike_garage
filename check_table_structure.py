#!/usr/bin/env python
"""
בדיקת מבנה הטבלה לאחר התיקון
"""
import os
import django
from django.db import connection

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def check_table_structure():
    """בדיקת מבנה הטבלה workshop_repairjob"""
    print("🔍 בודק את מבנה הטבלה workshop_repairjob...")
    
    with connection.cursor() as cursor:
        # בדיקת מבנה הטבלה
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'workshop_repairjob' 
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("\n📋 מבנה הטבלה:")
        print("-" * 80)
        for col in columns:
            col_name, data_type, max_length, nullable = col
            length_info = f" ({max_length})" if max_length else ""
            nullable_info = "NULL" if nullable == "YES" else "NOT NULL"
            print(f"{col_name:<30} {data_type}{length_info:<20} {nullable_info}")
        
        # בדיקה ספציפית לשדות שאמורים להיות קיימים
        required_fields = [
            'quality_checked_by_id',
            'quality_check_date', 
            'quality_notes',
            'ready_for_pickup_date',
            'customer_notified'
        ]
        
        existing_columns = [col[0] for col in columns]
        
        print("\n✅ בדיקת שדות נדרשים:")
        print("-" * 40)
        for field in required_fields:
            if field in existing_columns:
                print(f"✅ {field} - קיים")
            else:
                print(f"❌ {field} - חסר")
        
        # בדיקת אורך שדה status
        status_info = next((col for col in columns if col[0] == 'status'), None)
        if status_info:
            status_length = status_info[2]
            print(f"\n📏 שדה status: אורך {status_length}")
            if status_length >= 30:
                print("✅ אורך שדה status מספיק")
            else:
                print("❌ שדה status קצר מדי")

if __name__ == "__main__":
    check_table_structure()
