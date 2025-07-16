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

def debug_specific_repair():
    print("🔍 דיבוג תיקון ספציפי #16...")
    
    try:
        repair = RepairJob.objects.get(id=16)
        print(f"✅ נמצא תיקון #{repair.id}")
        print(f"   סטטוס: {repair.status}")
        print(f"   אופניים: {repair.bike}")
        print(f"   לקוח: {repair.bike.customer.name}")
        print(f"   מכונאי: {repair.assigned_mechanic}")
        
        # בדיקת הכללה ב-QuerySet של דשבורד
        awaiting_quality_check = RepairJob.objects.filter(status='awaiting_quality_check').select_related('bike', 'bike__customer', 'assigned_mechanic')
        
        print(f"\n📋 כל התיקונים ממתינים לבדיקת איכות:")
        for job in awaiting_quality_check:
            marker = "👉" if job.id == 16 else "  "
            print(f"{marker} תיקון #{job.id}: {job.bike.customer.name} - {job.status}")
        
        # בדיקה האם יש בעיה עם assigned_mechanic
        if repair.assigned_mechanic is None:
            print(f"⚠️ תיקון #{repair.id} לא מוקצה למכונאי!")
        
        # בדיקת has_quality_fields
        print(f"\n🛠️ has_quality_fields(): {has_quality_fields()}")
        
        # בדיקה ידנית של התמפלט
        from django.test import Client
        manager = User.objects.filter(userprofile__role='manager').first()
        if manager:
            client = Client()
            client.login(username=manager.username, password='test123')
            
            response = client.get('/manager/dashboard/')
            content = response.content.decode('utf-8')
            
            # חיפוש הקטע של בדיקת איכות
            import re
            
            # מחפש את הקטע הרלוונטי
            quality_section_match = re.search(
                r'ממתינים לבדיקת איכות.*?</div>\s*</div>',
                content,
                re.DOTALL
            )
            
            if quality_section_match:
                quality_section = quality_section_match.group(0)
                print(f"\n📄 קטע בדיקת איכות:")
                
                # מחפש מזהי תיקונים בקטע זה
                repair_ids_in_section = re.findall(r'<td>(\d+)</td>', quality_section)
                print(f"   מזהי תיקונים בקטע: {repair_ids_in_section}")
                
                if '16' in repair_ids_in_section:
                    print(f"   ✅ תיקון #16 נמצא בקטע!")
                else:
                    print(f"   ❌ תיקון #16 לא נמצא בקטע")
                    print(f"   🔍 מחפש '16' בכל הקטע: {'16' in quality_section}")
                    
                    # דוגמת התוכן
                    if len(quality_section) > 500:
                        print(f"\n📝 דוגמה מהקטע (ראשונות 500 תווים):")
                        print(quality_section[:500])
                    else:
                        print(f"\n📝 כל הקטע:")
                        print(quality_section)
            else:
                print(f"\n❌ לא נמצא קטע בדיקת איכות")
                
                # חיפוש כל הזכרות של 'ממתינים לבדיקת איכות'
                quality_mentions = re.findall(r'ממתינים לבדיקת איכות[^<]*', content)
                print(f"📋 הזכרות של בדיקת איכות: {quality_mentions}")
        
    except RepairJob.DoesNotExist:
        print(f"❌ תיקון #16 לא קיים")
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_specific_repair()
