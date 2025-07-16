import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# Setup Django
django.setup()

from workshop.views import has_quality_fields

def test_quality_fields():
    print("🔍 בדיקת שדות בדיקת איכות...")
    
    result = has_quality_fields()
    print(f"has_quality_fields() מחזיר: {result}")
    
    # בדיקה ידנית של השדות
    from django.db import connection
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(workshop_repairjob);")
        columns = [row[1] for row in cursor.fetchall()]
        
        print(f"\n📋 כל העמודות בטבלה ({len(columns)}):")
        for col in sorted(columns):
            print(f"   - {col}")
        
        required_fields = ['quality_checked_by_id', 'quality_check_date', 'quality_notes']
        print(f"\n🎯 שדות נדרשים לבדיקת איכות:")
        for field in required_fields:
            exists = field in columns
            status = "✅" if exists else "❌"
            print(f"   {status} {field}")
        
        missing = [field for field in required_fields if field not in columns]
        if missing:
            print(f"\n⚠️ שדות חסרים: {missing}")
        else:
            print(f"\n✅ כל השדות הנדרשים קיימים!")
            
    except Exception as e:
        print(f"\n❌ שגיאה בבדיקת טבלה: {e}")

if __name__ == "__main__":
    test_quality_fields()
