import os
import django
import sqlite3

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection

def fix_migrations():
    """תיקון migrations לטבלת workshop_repairjob"""
    
    cursor = connection.cursor()
    
    try:
        # בדיקה אם migration כבר קיים
        cursor.execute("""
            SELECT id FROM django_migrations 
            WHERE app = 'workshop' AND name = '0005_add_stuck_fields'
        """)
        
        if cursor.fetchone():
            print("✅ Migration 0005_add_stuck_fields כבר מסומן כמורץ")
        else:
            # הוספת migration לטבלה
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0005_add_stuck_fields', datetime('now'))
            """)
            print("✅ Migration 0005_add_stuck_fields נוסף לטבלה")
        
        # בדיקה שכל השדות קיימים
        cursor.execute("PRAGMA table_info(workshop_repairjob)")
        columns = [col[1] for col in cursor.fetchall()]
        
        required_fields = ['is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response']
        missing_fields = [field for field in required_fields if field not in columns]
        
        if missing_fields:
            print(f"⚠️  שדות חסרים: {missing_fields}")
            
            # הוספת שדות חסרים
            for field in missing_fields:
                if field == 'is_stuck':
                    cursor.execute("ALTER TABLE workshop_repairjob ADD COLUMN is_stuck BOOLEAN DEFAULT 0")
                elif field == 'stuck_reason':
                    cursor.execute("ALTER TABLE workshop_repairjob ADD COLUMN stuck_reason TEXT DEFAULT ''")
                elif field == 'stuck_at':
                    cursor.execute("ALTER TABLE workshop_repairjob ADD COLUMN stuck_at DATETIME")
                elif field == 'stuck_resolved':
                    cursor.execute("ALTER TABLE workshop_repairjob ADD COLUMN stuck_resolved BOOLEAN DEFAULT 0")
                elif field == 'manager_response':
                    cursor.execute("ALTER TABLE workshop_repairjob ADD COLUMN manager_response TEXT DEFAULT ''")
                
                print(f"✅ נוסף שדה: {field}")
        else:
            print("✅ כל השדות הנדרשים קיימים")
        
        connection.commit()
        print("\n🎉 תיקון migrations הושלם בהצלחה!")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        connection.rollback()

if __name__ == "__main__":
    fix_migrations()
