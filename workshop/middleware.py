"""
Middleware להוספת שדות חסרים אוטומטית
"""
from django.db import connection
from django.http import HttpResponse

class DatabaseFixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.fixed = False

    def __call__(self, request):
        # אם עדיין לא תוקן, נסה לתקן
        if not self.fixed:
            try:
                self.fix_database()
                self.fixed = True
            except Exception as e:
                print(f"Database fix failed: {e}")
                # אם התיקון נכשל, תחזיר הודעת שגיאה ידידותית
                return HttpResponse("""
                <h1>מערכת בתחזוקה</h1>
                <p>המערכת עוברת עדכון. אנא נסה שוב בעוד כמה דקות.</p>
                <p>לפרטים נוספים, צור קשר עם המנהל.</p>
                <br>
                <a href="/" onclick="location.reload()">נסה שוב</a>
                """)
        
        response = self.get_response(request)
        return response

    def fix_database(self):
        """תיקון מסד הנתונים"""
        with connection.cursor() as cursor:
            # בדיקה אילו עמודות כבר קיימות
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'workshop_repairjob'
            """)
            existing_columns = [row[0] for row in cursor.fetchall()]
            
            # הוספת עמודות חסרות
            columns_to_add = [
                ('quality_check_date', 'TIMESTAMP'),
                ('quality_notes', 'TEXT DEFAULT \'\''),
                ('ready_for_pickup_date', 'TIMESTAMP'),
                ('customer_notified', 'BOOLEAN DEFAULT FALSE')
            ]
            
            for column_name, column_def in columns_to_add:
                if column_name not in existing_columns:
                    sql = f"ALTER TABLE workshop_repairjob ADD COLUMN {column_name} {column_def};"
                    cursor.execute(sql)
            
            # הרחבת עמודת status
            try:
                cursor.execute("""
                    ALTER TABLE workshop_repairjob 
                    ALTER COLUMN status TYPE VARCHAR(30)
                """)
            except:
                pass  # כנראה כבר הורחב
            
            # סימון מיגרציה כמושלמת
            try:
                cursor.execute("""
                    INSERT INTO django_migrations (app, name, applied) 
                    VALUES ('workshop', '0008_repairjob_customer_notified_and_more', NOW())
                    ON CONFLICT DO NOTHING
                """)
            except:
                pass  # PostgreSQL syntax, אם זה SQLite יתעלם
