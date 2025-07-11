import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection

def mark_migration_as_applied():
    cursor = connection.cursor()
    
    # בדיקה אם migration כבר מסומן
    cursor.execute("""
        SELECT * FROM django_migrations 
        WHERE app = 'workshop' AND name = '0005_add_stuck_fields'
    """)
    result = cursor.fetchone()
    
    if result:
        print("Migration 0005_add_stuck_fields כבר מסומן כמורץ")
    else:
        # סימון migration כמורץ
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('workshop', '0005_add_stuck_fields', datetime('now'))
        """)
        print("Migration 0005_add_stuck_fields סומן כמורץ")
    
    # עדכון תלויות של migration 0006
    cursor.execute("""
        UPDATE django_migrations 
        SET name = '0005_add_stuck_fields' 
        WHERE app = 'workshop' AND name = '0005_add_stuck_fields'
    """)
    
    connection.commit()
    print("הושלם עדכון migrations")

if __name__ == "__main__":
    mark_migration_as_applied()
