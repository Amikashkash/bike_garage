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

def check_dashboard_html():
    print("🔍 בדיקת HTML מלא של דשבורד...")
    
    manager = User.objects.filter(userprofile__role='manager').first()
    if not manager:
        print("❌ לא נמצא מנהל")
        return
    
    client = Client()
    client.login(username=manager.username, password='test123')
    
    response = client.get('/manager/dashboard/')
    content = response.content.decode('utf-8')
    
    # שמירת כל ה-HTML לקובץ
    with open('full_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("💾 HTML מלא נשמר ל-full_dashboard.html")
    
    # חיפוש ספציפי של תיקון 16
    print(f"\n🔍 חיפוש תיקון 16:")
    
    # חיפוש כל המקומות שבהם מופיע 16
    lines_with_16 = []
    for i, line in enumerate(content.split('\n'), 1):
        if '16' in line:
            lines_with_16.append((i, line.strip()))
    
    print(f"📋 שורות עם '16' ({len(lines_with_16)}):")
    for line_num, line in lines_with_16[:10]:  # 10 הראשונות
        print(f"   {line_num}: {line}")
    
    # חיפוש הביטוי "ממתינים לבדיקת איכות"
    quality_count = content.count('ממתינים לבדיקת איכות')
    print(f"\n📊 'ממתינים לבדיקת איכות' מופיע {quality_count} פעמים")
    
    # בדיקה אם הקטע מוצג בכלל
    if 'awaiting_quality_check' in content or 'ממתינים לבדיקת איכות' in content:
        print("✅ קטע בדיקת איכות קיים")
        
        # חיפוש טבלת בדיקת איכות
        import re
        table_match = re.search(
            r'ממתינים לבדיקת איכות.*?</table>',
            content,
            re.DOTALL
        )
        
        if table_match:
            table_content = table_match.group(0)
            print(f"\n📄 תוכן טבלת בדיקת איכות:")
            
            # חיפוש שורות טבלה
            row_matches = re.findall(r'<tr.*?</tr>', table_content, re.DOTALL)
            print(f"📊 מספר שורות בטבלה: {len(row_matches)}")
            
            for i, row in enumerate(row_matches):
                if '<td>' in row:  # רק שורות נתונים
                    print(f"   שורה {i}: {row[:100]}...")
                    if '16' in row:
                        print(f"     👉 שורה זו מכילה 16!")
        else:
            print("❌ לא נמצאה טבלת בדיקת איכות")
    else:
        print("❌ קטע בדיקת איכות לא קיים")
    
    # ספירת מספר התיקונים ממתינים לבדיקת איכות
    actual_count = RepairJob.objects.filter(status='awaiting_quality_check').count()
    print(f"\n📈 מספר אמיתי בDB: {actual_count} תיקונים ממתינים לבדיקת איכות")
    
    # חיפוש המספר בתמפלט
    count_in_template = re.search(r'ממתינים לבדיקת איכות \((\d+)\)', content)
    if count_in_template:
        template_count = count_in_template.group(1)
        print(f"📊 מספר בתמפלט: {template_count}")
        
        if str(actual_count) == template_count:
            print("✅ המספר בתמפלט תואם למספר האמיתי")
        else:
            print("❌ המספר בתמפלט לא תואם למספר האמיתי!")
    else:
        print("❌ לא נמצא מספר תיקונים בתמפלט")

if __name__ == "__main__":
    check_dashboard_html()
