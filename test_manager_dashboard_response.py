import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# Setup Django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from workshop.models import UserProfile

def test_manager_dashboard_response():
    print("🔍 בדיקת תגובת דשבורד מנהל...")
    
    User = get_user_model()
    
    # חיפוש או יצירת מנהל
    try:
        manager = User.objects.filter(userprofile__role='manager').first()
        if not manager:
            print("יוצר מנהל חדש...")
            manager = User.objects.create_user(
                username='manager_test',
                password='test123',
                first_name='מנהל',
                last_name='בדיקה'
            )
            UserProfile.objects.create(user=manager, role='manager')
        
        print(f"✅ נמצא מנהל: {manager.username}")
        
        # יצירת client ובדיקה
        client = Client()
        login_success = client.login(username=manager.username, password='test123')
        
        if not login_success:
            print("❌ כניסה נכשלה")
            return
        
        print("✅ הכניסה הצליחה")
        
        # קבלת דף דשבורד
        response = client.get('/manager/dashboard/')
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # חיפוש הביטוי "ממתינים לבדיקת איכות"
            if 'ממתינים לבדיקת איכות' in content:
                print("✅ הביטוי 'ממתינים לבדיקת איכות' נמצא בתגובה!")
                
                # ספירת התרחשויות
                count = content.count('ממתינים לבדיקת איכות')
                print(f"📊 מופיע {count} פעמים")
                
                # חיפוש מספר התיקונים
                import re
                pattern = r'ממתינים לבדיקת איכות \((\d+)\)'
                match = re.search(pattern, content)
                if match:
                    displayed_count = match.group(1)
                    print(f"📈 מספר תיקונים מוצג: {displayed_count}")
                
            else:
                print("❌ הביטוי 'ממתינים לבדיקת איכות' לא נמצא!")
            
            # חיפוש הכרטיס של בדיקת איכות
            if 'card border-warning' in content and 'fas fa-search' in content:
                print("✅ הכרטיס של בדיקת איכות נמצא!")
            else:
                print("❌ הכרטיס של בדיקת איכות לא נמצא")
            
            # בדיקה - אולי יש שגיאה בתמפלט
            if 'error' in content.lower():
                print("⚠️ יש שגיאה בתמפלט:")
                error_lines = [line.strip() for line in content.split('\n') if 'error' in line.lower()]
                for line in error_lines[:3]:  # 3 הראשונות
                    print(f"   {line}")
            
            # שמירת HTML לקובץ לבדיקה
            with open('manager_dashboard_debug.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("💾 התגובה נשמרה ל-manager_dashboard_debug.html")
            
        else:
            print(f"❌ שגיאה בגישה לדף: {response.status_code}")
            print(f"Content: {response.content.decode('utf-8')[:500]}")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_manager_dashboard_response()
