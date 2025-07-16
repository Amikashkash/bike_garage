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
from django.test import Client

def test_mechanic_completion_workflow():
    print("🔧 בדיקת זרימה: מכונאי מסיים תיקון...")
    
    # מוצא תיקון שבביצוע
    in_progress_repair = RepairJob.objects.filter(
        status__in=['approved', 'in_progress']
    ).first()
    
    if not in_progress_repair:
        print("❌ לא נמצא תיקון בביצוע")
        return
    
    print(f"✅ נמצא תיקון #{in_progress_repair.id} בסטטוס: {in_progress_repair.status}")
    
    # מוצא מכונאי
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    if not mechanic:
        print("❌ לא נמצא מכונאי")
        return
    
    print(f"✅ מכונאי: {mechanic.username}")
    
    # בדיקה לפני - כמה ממתינים לבדיקת איכות
    before_count = RepairJob.objects.filter(status='awaiting_quality_check').count()
    print(f"📊 לפני הסיום: {before_count} תיקונים ממתינים לבדיקת איכות")
    
    # סימולציה - המכונאי מסיים את התיקון
    if in_progress_repair.assigned_mechanic != mechanic:
        in_progress_repair.assigned_mechanic = mechanic
        in_progress_repair.save()
    
    # מעבר לסטטוס ממתין לבדיקת איכות (כפי שקורה בטופס השלמת משימה)
    in_progress_repair.status = 'awaiting_quality_check'
    in_progress_repair.save()
    
    print(f"✅ תיקון #{in_progress_repair.id} עודכן לסטטוס: {in_progress_repair.status}")
    
    # בדיקה אחרי - כמה ממתינים לבדיקת איכות
    after_count = RepairJob.objects.filter(status='awaiting_quality_check').count()
    print(f"📊 אחרי הסיום: {after_count} תיקונים ממתינים לבדיקת איכות")
    
    if after_count > before_count:
        print(f"✅ נוסף תיקון לבדיקת איכות! (+{after_count - before_count})")
    else:
        print("⚠️ לא נוסף תיקון חדש")
    
    # בדיקת context של דשבורד המנהל
    print("\n🎯 בדיקת דשבורד מנהל...")
    
    try:
        # התחברות כמנהל ובדיקת דשבורד
        manager = User.objects.filter(userprofile__role='manager').first()
        if manager:
            client = Client()
            client.login(username=manager.username, password='test123')
            
            response = client.get('/manager/dashboard/')
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # חיפוש התיקון ברשימת בדיקת איכות
                if f'#{in_progress_repair.id}' in content and 'ממתינים לבדיקת איכות' in content:
                    print(f"✅ תיקון #{in_progress_repair.id} מופיע בדשבורד המנהל!")
                else:
                    print(f"❌ תיקון #{in_progress_repair.id} לא מופיע בדשבורד")
                
                # ספירת מזהי תיקונים בקטע בדיקת איכות
                import re
                repair_ids = re.findall(r'#(\d+)', content)
                print(f"📋 מזהי תיקונים בדשבורד: {set(repair_ids)}")
                
            else:
                print(f"❌ שגיאה בגישה לדשבורד: {response.status_code}")
        else:
            print("❌ לא נמצא מנהל")
            
    except Exception as e:
        print(f"❌ שגיאה בבדיקת דשבורד: {e}")
    
    return in_progress_repair.id

if __name__ == "__main__":
    repair_id = test_mechanic_completion_workflow()
    print(f"\n🔄 כעת רענן את הדשבורד בדפדפן ובדוק שתיקון #{repair_id} מופיע בבקרת איכות")
