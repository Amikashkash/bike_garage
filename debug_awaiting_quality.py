import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# Setup Django
django.setup()

from workshop.models import RepairJob

def debug_awaiting_quality():
    print("🔍 דיבוג תיקונים ממתינים לבדיקת איכות...")
    
    awaiting = RepairJob.objects.filter(status='awaiting_quality_check').select_related('bike', 'bike__customer', 'assigned_mechanic')
    
    print(f"📊 כל התיקונים ממתינים לבדיקת איכות ({awaiting.count()}):")
    
    for repair in awaiting:
        print(f"\n   תיקון #{repair.id}:")
        print(f"     סטטוס: {repair.status}")
        print(f"     אופניים: {repair.bike}")
        print(f"     לקוח: {repair.bike.customer.name}")
        print(f"     מכונאי: {repair.assigned_mechanic}")
        print(f"     created_at: {repair.created_at}")
        
        # בדיקה אם השדות נדרשים קיימים
        has_bike = repair.bike is not None
        has_customer = repair.bike and repair.bike.customer is not None
        has_mechanic = repair.assigned_mechanic is not None
        
        print(f"     יש אופניים: {has_bike}")
        print(f"     יש לקוח: {has_customer}")
        print(f"     יש מכונאי: {has_mechanic}")
        
        # בדיקה אם הקשרים תקינים
        try:
            customer_name = repair.bike.customer.name
            bike_str = str(repair.bike)
            mechanic_name = repair.assigned_mechanic.first_name if repair.assigned_mechanic else "אין"
            print(f"     ✅ כל הקשרים תקינים")
        except Exception as e:
            print(f"     ❌ בעיה בקשרים: {e}")

if __name__ == "__main__":
    debug_awaiting_quality()
