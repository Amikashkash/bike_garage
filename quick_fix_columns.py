#!/usr/bin/env python
"""
סקריפט להוספה מהירה של שדות חסרים למסד נתונים בשרת
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
import sys

def quick_add_missing_columns():
    """הוספה מהירה של עמודות חסרות"""
    print("🚨 הוספה מהירה של עמודות בדיקת איכות...")
    
    cursor = connection.cursor()
    
    # רשימת העמודות שצריך להוסיף
    columns_to_add = [
        ('quality_checked_by_id', 'INTEGER REFERENCES auth_user(id)'),
        ('quality_check_date', 'DATETIME'),
        ('quality_notes', 'TEXT DEFAULT ""'),
        ('ready_for_pickup_date', 'DATETIME'),
        ('customer_notified', 'BOOLEAN DEFAULT FALSE')
    ]
    
    # בדיקה אילו עמודות כבר קיימות
    cursor.execute("PRAGMA table_info(workshop_repairjob);")
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    success_count = 0
    
    for column_name, column_def in columns_to_add:
        if column_name not in existing_columns:
            try:
                sql = f"ALTER TABLE workshop_repairjob ADD COLUMN {column_name} {column_def};"
                print(f"📝 מוסיף: {column_name}")
                cursor.execute(sql)
                success_count += 1
                print(f"✅ {column_name} נוסף בהצלחה")
            except Exception as e:
                print(f"❌ שגיאה בהוספת {column_name}: {e}")
        else:
            print(f"⏭️ {column_name} כבר קיים")
    
    print(f"\n📊 סיכום: {success_count} עמודות נוספו")
    
    # בדיקה סופית
    cursor.execute("PRAGMA table_info(workshop_repairjob);")
    final_columns = [row[1] for row in cursor.fetchall()]
    
    missing = [col for col, _ in columns_to_add if col not in final_columns]
    
    if not missing:
        print("✅ כל העמודות הוספו בהצלחה!")
        return True
    else:
        print(f"❌ עדיין חסרות עמודות: {missing}")
        return False

def test_repair_creation():
    """בדיקה שניתן ליצור תיקון חדש"""
    try:
        from workshop.models import RepairJob, Customer, Bike
        
        print("\n🧪 בדיקת יצירת תיקון...")
        
        # חיפוש לקוח ואופניים קיימים
        customer = Customer.objects.first()
        if not customer:
            print("❌ לא נמצא לקוח במערכת")
            return False
            
        bike = customer.bikes.first()
        if not bike:
            print("❌ לא נמצאו אופניים")
            return False
        
        # ניסיון ליצור תיקון פשוט
        repair = RepairJob(
            bike=bike,
            problem_description="בדיקה שהמערכת עובדת",
            status='reported'
        )
        repair.save()
        
        print(f"✅ תיקון נוצר בהצלחה: #{repair.id}")
        
        # מחיקת התיקון אחרי הבדיקה
        repair.delete()
        print("🗑️ תיקון בדיקה נמחק")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת תיקון: {e}")
        return False

if __name__ == "__main__":
    print("🔧 תיקון מהיר לשדות חסרים")
    print("=" * 40)
    
    # הוספת עמודות
    columns_added = quick_add_missing_columns()
    
    if columns_added:
        # בדיקת יצירת תיקון
        repair_works = test_repair_creation()
        
        if repair_works:
            print("\n🎉 תיקון הושלם! המערכת אמורה לעבוד כעת")
        else:
            print("\n⚠️ עדיין יש בעיות ביצירת תיקונים")
    else:
        print("\n❌ לא ניתן להוסיף עמודות. נדרש תיקון ידני")
