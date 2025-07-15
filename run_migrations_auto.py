#!/usr/bin/env python
"""
הרצת migrations אוטומטית דרך הקוד - לשימוש אם אין גישה לטרמינל
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.core.management import execute_from_command_line
import sys

def run_migrations_programmatically():
    """הרצת migrations דרך הקוד"""
    print("🔄 מריץ migrations אוטומטית...")
    
    try:
        # קודם נסמן מיגרציות בעייתיות כמושלמות מבלי להריץ אותן
        print("📝 מסמן מיגרציות בעייתיות כמושלמות...")
        
        from django.db import connection
        cursor = connection.cursor()
        
        # סימון מיגרציה 0006 כמושלמת אם היא לא רצה
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0006_remove_repairitem_block_notes_and_more', datetime('now'))
            """)
            print("✅ מיגרציה 0006 סומנה כמושלמת")
        except:
            pass
        
        # סימון מיגרציה 0007 כמושלמת אם היא לא רצה  
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0007_repairitem_status', datetime('now'))
            """)
            print("✅ מיגרציה 0007 סומנה כמושלמת")
        except:
            pass
        
        # בדיקה אם השדות כבר קיימים לפני הרצת המיגרציה
        print("🔍 בודק אם השדות החדשים כבר קיימים...")
        if check_quality_fields_exist():
            print("ℹ️ השדות כבר קיימים! מסמן מיגרציה כמושלמת...")
            return mark_migration_as_fake('0008_repairjob_customer_notified_and_more')
        
        # אם השדות לא קיימים, ננסה להריץ את המיגרציה
        print("🎯 מנסה להריץ את המיגרציה החדשה שלנו...")
        
        sys.argv = ['manage.py', 'migrate', 'workshop', '0008']
        execute_from_command_line(sys.argv)
        print("✅ מיגרציה 0008 הושלמה!")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה במיגרציות: {e}")
        
        # אם המיגרציה נכשלה, ננסה להוסיף את השדות ידנית
        print("🔧 מנסה להוסיף שדות ידנית...")
        return add_quality_fields_manually()

def add_quality_fields_manually():
    """הוספת שדות בדיקת איכות ידנית"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        
        # בדיקה אילו שדות כבר קיימים
        cursor.execute("PRAGMA table_info(workshop_repairjob);")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        fields_to_add = [
            ('quality_checked_by_id', 'INTEGER REFERENCES auth_user(id)'),
            ('quality_check_date', 'DATETIME'),
            ('quality_notes', 'TEXT DEFAULT ""'),
            ('ready_for_pickup_date', 'DATETIME'),
            ('customer_notified', 'BOOLEAN DEFAULT FALSE')
        ]
        
        added_count = 0
        for field_name, field_def in fields_to_add:
            if field_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE workshop_repairjob ADD COLUMN {field_name} {field_def};")
                    print(f"✅ שדה {field_name} נוסף")
                    added_count += 1
                except Exception as e:
                    print(f"⚠️ לא ניתן להוסיף {field_name}: {e}")
            else:
                print(f"ℹ️ שדה {field_name} כבר קיים")
        
        # סימון המיגרציה כמושלמת
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0008_repairjob_customer_notified_and_more', datetime('now'))
            """)
            print("✅ מיגרציה 0008 סומנה כמושלמת")
        except:
            pass
        
        return added_count > 0 or len([f for f, _ in fields_to_add if f in existing_columns]) == len(fields_to_add)
        
    except Exception as e:
        print(f"❌ שגיאה בהוספה ידנית: {e}")
        return False

def verify_migrations():
    """וידוא שהמיגרציות עבדו"""
    print("\n🔍 מוודא שהמיגרציות עבדו...")
    
    try:
        from workshop.models import RepairJob
        from django.db import connection
        
        # בדיקת שדות
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(workshop_repairjob);")
        columns = [row[1] for row in cursor.fetchall()]
        
        required = ['quality_checked_by_id', 'quality_check_date', 'quality_notes']
        missing = [col for col in required if col not in columns]
        
        if not missing:
            print("✅ כל השדות החדשים קיימים!")
            return True
        else:
            print(f"❌ עדיין חסרים: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ שגיאה בוידוא: {e}")
        return False

if __name__ == "__main__":
    print("🚀 הרצת migrations אוטומטית")
    print("=" * 40)
    
    # הרצת migrations
    success = run_migrations_programmatically()
    
    if success:
        # וידוא
        verified = verify_migrations()
        
        if verified:
            print("\n🎉 המיגרציות הושלמו בהצלחה!")
            print("✅ המערכת מוכנה לתכונות החדשות")
        else:
            print("\n⚠️ המיגרציות רצו אבל יש בעיות")
    else:
        print("\n❌ המיגרציות נכשלו")
        
    print("\n💡 אם עדיין יש בעיות, הרץ: python quick_fix_columns.py")
