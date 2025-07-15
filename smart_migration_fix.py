#!/usr/bin/env python
"""
תיקון חכם למיגרציות - בדיקה ותיקון של שדות קיימים לעומת חסרים
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection, transaction
from django.core.management import execute_from_command_line
import sys

def get_current_schema():
    """קבלת הסכמה נוכחית של הטבלה"""
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(workshop_repairjob);")
    return {row[1]: row[2] for row in cursor.fetchall()}  # {column_name: column_type}

def get_expected_schema():
    """רשימת השדות שאמורים להיות בטבלה"""
    return {
        # שדות בסיסיים
        'id': 'INTEGER',
        'bike_id': 'INTEGER',
        'problem_description': 'TEXT',
        'diagnosis': 'TEXT',
        'status': 'VARCHAR(30)',
        'created_at': 'DATETIME',
        'diagnosed_at': 'DATETIME',
        'approved_at': 'DATETIME',
        
        # שדות מכונאי וניהול
        'assigned_mechanic_id': 'INTEGER',
        'is_stuck': 'BOOLEAN',
        'stuck_reason': 'TEXT',
        'stuck_at': 'DATETIME',
        'stuck_resolved': 'BOOLEAN',
        'manager_response': 'TEXT',
        
        # שדות בדיקת איכות חדשים
        'quality_checked_by_id': 'INTEGER',
        'quality_check_date': 'DATETIME',
        'quality_notes': 'TEXT',
        'ready_for_pickup_date': 'DATETIME',
        'customer_notified': 'BOOLEAN'
    }

def smart_add_missing_columns():
    """הוספה חכמה של עמודות חסרות בלבד"""
    print("🔍 בודק סכמה נוכחית...")
    
    current_schema = get_current_schema()
    expected_schema = get_expected_schema()
    
    print(f"📊 עמודות קיימות: {len(current_schema)}")
    print(f"📊 עמודות צפויות: {len(expected_schema)}")
    
    # מציאת עמודות חסרות
    missing_columns = []
    for col_name, col_type in expected_schema.items():
        if col_name not in current_schema:
            missing_columns.append((col_name, col_type))
    
    if not missing_columns:
        print("✅ כל העמודות קיימות!")
        return True
    
    print(f"\n📝 נמצאו {len(missing_columns)} עמודות חסרות:")
    for col_name, col_type in missing_columns:
        print(f"   - {col_name} ({col_type})")
    
    # הוספת עמודות חסרות
    cursor = connection.cursor()
    success_count = 0
    
    try:
        with transaction.atomic():
            for col_name, col_type in missing_columns:
                try:
                    # הגדרת ברירת מחדל לפי סוג השדה
                    default_value = ""
                    if col_type == 'BOOLEAN':
                        default_value = "DEFAULT FALSE"
                    elif col_type == 'TEXT':
                        default_value = "DEFAULT ''"
                    elif col_type == 'INTEGER':
                        default_value = "DEFAULT NULL"
                    elif col_type == 'DATETIME':
                        default_value = "DEFAULT NULL"
                    elif 'VARCHAR' in col_type:
                        default_value = "DEFAULT 'reported'" if col_name == 'status' else "DEFAULT ''"
                    
                    sql = f"ALTER TABLE workshop_repairjob ADD COLUMN {col_name} {col_type} {default_value};"
                    print(f"📝 מוסיף: {col_name}...")
                    cursor.execute(sql)
                    success_count += 1
                    print(f"✅ {col_name} נוסף בהצלחה")
                    
                except Exception as e:
                    print(f"❌ שגיאה בהוספת {col_name}: {e}")
                    # אל תעצור - המשך עם השדות הבאים
        
        print(f"\n📊 הוספו {success_count}/{len(missing_columns)} עמודות")
        return success_count == len(missing_columns)
        
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
        return False

def fix_migrations_table():
    """תיקון טבלת המיגרציות כדי למנוע הרצה חוזרת"""
    print("\n🔧 מתקן טבלת migrations...")
    
    try:
        cursor = connection.cursor()
        
        # בדיקה אם המיגרציה האחרונה רשומה
        cursor.execute("""
            SELECT name FROM django_migrations 
            WHERE app = 'workshop' AND name LIKE '%quality%'
        """)
        
        existing_migrations = [row[0] for row in cursor.fetchall()]
        
        if not existing_migrations:
            # רישום המיגרציה כמושלמת
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0008_repairjob_customer_notified_and_more', datetime('now'))
            """)
            print("✅ מיגרציה נרשמה כמושלמת")
        else:
            print("ℹ️ מיגרציה כבר רשומה")
            
        return True
        
    except Exception as e:
        print(f"⚠️ לא ניתן לעדכן טבלת migrations: {e}")
        return False

def verify_final_state():
    """וידוא סופי שהכל תקין"""
    print("\n🔍 בדיקה סופית...")
    
    try:
        from workshop.models import RepairJob
        
        # ניסיון ליצור תיקון
        print("🧪 בודק יצירת תיקון...")
        
        # בדיקה שניתן לגשת לכל השדות החדשים
        current_schema = get_current_schema()
        new_fields = ['quality_checked_by_id', 'quality_check_date', 'quality_notes', 
                     'ready_for_pickup_date', 'customer_notified']
        
        missing = [field for field in new_fields if field not in current_schema]
        
        if not missing:
            print("✅ כל השדות החדשים זמינים")
            
            # בדיקת סטטוסים חדשים
            try:
                awaiting_count = RepairJob.objects.filter(status='awaiting_quality_check').count()
                approved_count = RepairJob.objects.filter(status='quality_approved').count()
                print(f"✅ סטטוסים חדשים עובדים (ממתינים: {awaiting_count}, מאושרים: {approved_count})")
                return True
            except Exception as e:
                print(f"⚠️ בעיה בסטטוסים חדשים: {e}")
                return False
        else:
            print(f"❌ עדיין חסרים שדות: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ שגיאה בבדיקה סופית: {e}")
        return False

def main():
    """תהליך התיקון המלא"""
    print("🛠️ תיקון חכם למיגרציות")
    print("=" * 50)
    
    # שלב 1: הוספת עמודות חסרות
    columns_fixed = smart_add_missing_columns()
    
    # שלב 2: תיקון טבלת מיגרציות
    migrations_fixed = fix_migrations_table()
    
    # שלב 3: וידוא סופי
    if columns_fixed:
        final_ok = verify_final_state()
        
        if final_ok:
            print("\n🎉 תיקון הושלם בהצלחה!")
            print("✅ המערכת מוכנה לתכונות בדיקת האיכות")
            return True
        else:
            print("\n⚠️ התיקון חלקי - חלק מהתכונות עדיין לא זמינות")
            return False
    else:
        print("\n❌ התיקון נכשל")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n💡 עכשיו אפשר לבדוק את הדשבורד החדש!")
    else:
        print("\n💡 אם עדיין יש בעיות, פנה למפתח המערכת")
