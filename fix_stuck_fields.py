#!/usr/bin/env python
"""
תיקון חכם לשדות is_stuck - עובד עם SQLite ו-PostgreSQL
"""

import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection, transaction
from django.conf import settings

def get_db_type():
    """זיהוי סוג מסד הנתונים"""
    engine = settings.DATABASES['default']['ENGINE']
    if 'sqlite' in engine:
        return 'sqlite'
    elif 'postgresql' in engine:
        return 'postgresql'
    else:
        return 'unknown'

def check_column_exists(table_name, column_name):
    """בדיקה אם עמודה קיימת"""
    cursor = connection.cursor()
    db_type = get_db_type()
    
    try:
        if db_type == 'sqlite':
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            return column_name in columns
        
        elif db_type == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = %s
            """, [table_name, column_name])
            return cursor.fetchone() is not None
        
        return False
    except Exception as e:
        print(f"שגיאה בבדיקת עמודה {column_name}: {e}")
        return False

def add_column_safe(table_name, column_name, column_definition):
    """הוספת עמודה בצורה בטוחה"""
    if check_column_exists(table_name, column_name):
        print(f"✅ עמודה {column_name} כבר קיימת")
        return True
    
    cursor = connection.cursor()
    db_type = get_db_type()
    
    try:
        if db_type == 'sqlite':
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_definition}")
        elif db_type == 'postgresql':
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_definition}")
        
        print(f"✅ נוספה עמודה {column_name}")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בהוספת עמודה {column_name}: {e}")
        return False

def mark_migration_applied():
    """סימון migration כמורץ"""
    cursor = connection.cursor()
    
    try:
        # בדיקה אם migration כבר קיים
        cursor.execute("""
            SELECT id FROM django_migrations 
            WHERE app = 'workshop' AND name = '0005_add_stuck_fields'
        """)
        
        if cursor.fetchone():
            print("✅ Migration 0005_add_stuck_fields כבר מסומן")
            return True
        
        # הוספת migration
        db_type = get_db_type()
        if db_type == 'sqlite':
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0005_add_stuck_fields', datetime('now'))
            """)
        elif db_type == 'postgresql':
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0005_add_stuck_fields', NOW())
            """)
        
        print("✅ Migration 0005_add_stuck_fields נוסף")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בסימון migration: {e}")
        return False

def fix_stuck_fields():
    """תיקון שדות is_stuck בטבלת RepairJob"""
    print("🔧 תיקון שדות is_stuck...")
    print(f"💾 סוג מסד נתונים: {get_db_type()}")
    
    # רשימת השדות להוסיף
    fields_to_add = [
        ('is_stuck', 'is_stuck BOOLEAN DEFAULT FALSE'),
        ('stuck_reason', 'stuck_reason TEXT DEFAULT \'\''),
        ('stuck_at', 'stuck_at TIMESTAMP NULL'),
        ('stuck_resolved', 'stuck_resolved BOOLEAN DEFAULT FALSE'),
        ('manager_response', 'manager_response TEXT DEFAULT \'\'')
    ]
    
    success_count = 0
    
    with transaction.atomic():
        for field_name, field_definition in fields_to_add:
            if add_column_safe('workshop_repairjob', field_name, field_definition):
                success_count += 1
        
        # סימון migration כמורץ
        if mark_migration_applied():
            success_count += 1
    
    print(f"\n🎉 הושלם תיקון {success_count}/{len(fields_to_add)+1} פריטים")
    
    if success_count == len(fields_to_add) + 1:
        print("✅ כל התיקונים הושלמו בהצלחה!")
        return True
    else:
        print("⚠️ חלק מהתיקונים נכשלו")
        return False

def main():
    try:
        print("🚀 מתחיל תיקון שדות is_stuck...")
        success = fix_stuck_fields()
        
        if success:
            print("\n✅ תיקון הושלם בהצלחה!")
            print("המערכת אמורה לעבוד כעת")
        else:
            print("\n❌ תיקון נכשל חלקית")
            
    except Exception as e:
        print(f"\n💥 שגיאה כללית: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
