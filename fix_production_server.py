#!/usr/bin/env python
"""
תיקון אוטומטי לשרת ייצור - הוספת שדות חסרים
"""
import os
import django
from django.core.management import execute_from_command_line

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection

def add_missing_columns_production():
    """הוספת עמודות חסרות בשרת ייצור"""
    print("🔧 מוסיף עמודות חסרות בשרת ייצור...")
    
    try:
        with connection.cursor() as cursor:
            # בדיקה אילו עמודות כבר קיימות
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'workshop_repairjob'
            """)
            existing_columns = [row[0] for row in cursor.fetchall()]
            print(f"עמודות קיימות: {existing_columns}")
            
            # רשימת עמודות שצריך להוסיף
            columns_to_add = [
                ('quality_check_date', 'TIMESTAMP'),
                ('quality_notes', 'TEXT DEFAULT \'\''),
                ('ready_for_pickup_date', 'TIMESTAMP'),
                ('customer_notified', 'BOOLEAN DEFAULT FALSE')
            ]
            
            # הוספת עמודות חסרות
            added_count = 0
            for column_name, column_def in columns_to_add:
                if column_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE workshop_repairjob ADD COLUMN {column_name} {column_def};"
                        cursor.execute(sql)
                        print(f"✅ נוסף: {column_name}")
                        added_count += 1
                    except Exception as e:
                        print(f"❌ שגיאה בהוספת {column_name}: {e}")
                else:
                    print(f"ℹ️ כבר קיים: {column_name}")
            
            # הרחבת עמודת status אם צריך
            try:
                cursor.execute("""
                    ALTER TABLE workshop_repairjob 
                    ALTER COLUMN status TYPE VARCHAR(30)
                """)
                print("✅ עמודת status הורחבה ל-30 תווים")
            except Exception as e:
                print(f"ℹ️ עמודת status: {e}")
            
            print(f"\n✅ הושלם! נוספו {added_count} עמודות")
            return True
            
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
        import traceback
        traceback.print_exc()
        return False

def mark_migration_as_applied():
    """סימון מיגרציה 0008 כמושלמת"""
    try:
        with connection.cursor() as cursor:
            # בדיקה אם המיגרציה כבר קיימת
            cursor.execute("""
                SELECT COUNT(*) FROM django_migrations 
                WHERE app = 'workshop' AND name = '0008_repairjob_customer_notified_and_more'
            """)
            exists = cursor.fetchone()[0]
            
            if not exists:
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('workshop', '0008_repairjob_customer_notified_and_more', NOW())
                """)
                print("✅ מיגרציה 0008 סומנה כמושלמת")
            else:
                print("ℹ️ מיגרציה 0008 כבר קיימת")
                
    except Exception as e:
        print(f"❌ שגיאה בסימון מיגרציה: {e}")

def main():
    """תהליך תיקון ראשי"""
    print("🚀 מתחיל תיקון שרת ייצור...")
    
    # שלב 1: הוספת עמודות
    success = add_missing_columns_production()
    
    if success:
        # שלב 2: סימון מיגרציה
        mark_migration_as_applied()
        
        print("\n🎉 תיקון שרת הושלם בהצלחה!")
        print("💡 עכשיו אפשר להפעיל מחדש את השרת")
    else:
        print("\n❌ תיקון שרת נכשל")

if __name__ == "__main__":
    main()
