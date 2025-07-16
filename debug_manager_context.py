import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# Setup Django
django.setup()

from workshop.models import RepairJob, User
from workshop.views import has_quality_fields

def debug_manager_dashboard_context():
    print("🔍 דיבוג context של דשבורד מנהל...")
    
    try:
        # בדיקה ראשונה - האם השדות קיימים
        quality_fields_exist = has_quality_fields()
        print(f"\n🛠️ has_quality_fields(): {quality_fields_exist}")
        
        # דמיון של הקוד בדשבורד המנהל
        awaiting_quality_check = []
        ready_for_pickup = []
        
        if quality_fields_exist:
            awaiting_quality_check = RepairJob.objects.filter(status='awaiting_quality_check').select_related('bike', 'bike__customer', 'assigned_mechanic')
            ready_for_pickup = RepairJob.objects.filter(status='quality_approved').select_related('bike', 'bike__customer')
            
            print(f"\n📋 awaiting_quality_check QuerySet:")
            print(f"   - Count: {awaiting_quality_check.count()}")
            for repair in awaiting_quality_check:
                print(f"   - תיקון #{repair.id}: {repair.bike.customer.name} - {repair.status}")
            
            print(f"\n📋 ready_for_pickup QuerySet:")
            print(f"   - Count: {ready_for_pickup.count()}")
            for repair in ready_for_pickup:
                print(f"   - תיקון #{repair.id}: {repair.bike.customer.name} - {repair.status}")
        else:
            print("\n⚠️ השדות לא קיימים - לא יוצרים QuerySet")
        
        # בדיקה - האם הם מוצגים בתמפלט
        print(f"\n🎯 תוצאת התנאי במקרה של awaiting_quality_check:")
        if awaiting_quality_check:
            print(f"   ✅ התנאי יעבור (יש {awaiting_quality_check.count()} תיקונים)")
        else:
            print(f"   ❌ התנאי לא יעבור (QuerySet ריק)")
        
        # בדיקה נוספת - כל התיקונים עם הסטטוס הזה
        all_awaiting = RepairJob.objects.filter(status='awaiting_quality_check')
        print(f"\n🔍 בדיקה ישירה - תיקונים עם status='awaiting_quality_check':")
        print(f"   Count: {all_awaiting.count()}")
        
        for repair in all_awaiting:
            print(f"   - #{repair.id}: {repair.bike.customer.name}")
            print(f"     Status: {repair.status}")
            print(f"     Assigned mechanic: {repair.assigned_mechanic}")
            
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_manager_dashboard_context()
