from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'הוספת שדות חסרים לטבלת RepairJob'

    def handle(self, *args, **options):
        self.stdout.write("🔧 מוסיף שדות חסרים...")
        
        try:
            with connection.cursor() as cursor:
                # בדיקה אילו עמודות כבר קיימות
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'workshop_repairjob'
                """)
                existing_columns = [row[0] for row in cursor.fetchall()]
                
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
                            self.stdout.write(f"✅ נוסף: {column_name}")
                            added_count += 1
                        except Exception as e:
                            self.stdout.write(f"❌ שגיאה בהוספת {column_name}: {e}")
                    else:
                        self.stdout.write(f"ℹ️ כבר קיים: {column_name}")
                
                # הרחבת עמודת status
                try:
                    cursor.execute("""
                        ALTER TABLE workshop_repairjob 
                        ALTER COLUMN status TYPE VARCHAR(30)
                    """)
                    self.stdout.write("✅ עמודת status הורחבה ל-30 תווים")
                except Exception as e:
                    self.stdout.write(f"ℹ️ עמודת status: {e}")
                
                # סימון מיגרציה כמושלמת
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('workshop', '0008_repairjob_customer_notified_and_more', NOW())
                    ON CONFLICT DO NOTHING
                """)
                
                self.stdout.write(f"\n✅ הושלם! נוספו {added_count} עמודות")
                
        except Exception as e:
            self.stdout.write(f"❌ שגיאה: {e}")
            import traceback
            traceback.print_exc()
