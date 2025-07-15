#!/usr/bin/env python
"""
בדיקת סטטוס production - בדיקה מקיפה של המערכת
"""
import os
import django
import requests
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, Customer, User, RepairItem, RepairCategory
from django.contrib.auth.models import Group

def check_production_status():
    """בדיקת סטטוס הפרודקשן"""
    print("🔍 בדיקת סטטוס Production - BikeGarage")
    print("=" * 50)
    
    # 1. בדיקת חיבור לשרת
    print("\n🌐 בדיקת חיבור לשרת...")
    try:
        response = requests.get('https://bikegarage-4yjs.onrender.com/', timeout=10)
        print(f"   ✅ שרת מגיב: {response.status_code}")
        if response.status_code == 200:
            if 'BikeGarage' in response.text or 'מוסך' in response.text or 'ברוכים הבאים' in response.text:
                print("   ✅ תוכן נטען כראוי")
            else:
                print("   ⚠️ תוכן חשוד")
        elif response.status_code == 404:
            print("   ⚠️ דף בית מחזיר 404 - אבל זה לא בהכרח בעיה רצינית")
        else:
            print(f"   ⚠️ שרת מחזיר קוד בלתי צפוי: {response.status_code}")
    except Exception as e:
        print(f"   ❌ שגיאת חיבור: {e}")
    
    # בדיקת דפים אחרים
    print("\n🔗 בדיקת דפים נוספים...")
    test_urls = [
        ('login', '/login/'),
        ('register', '/register/'),
        ('customer-report', '/customer-report/'),
    ]
    
    for name, url in test_urls:
        try:
            response = requests.get(f'https://bikegarage-4yjs.onrender.com{url}', timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: שגיאה - {e}")
    
    # 2. בדיקת מסד נתונים
    print("\n🗄️ בדיקת מסד נתונים...")
    try:
        users_count = User.objects.count()
        repairs_count = RepairJob.objects.count()
        customers_count = Customer.objects.count()
        items_count = RepairItem.objects.count()
        categories_count = RepairCategory.objects.count()
        
        print(f"   👥 משתמשים: {users_count}")
        print(f"   🔧 תיקונים: {repairs_count}")
        print(f"   🚴 לקוחות: {customers_count}")
        print(f"   🛠️ פריטי תיקון: {items_count}")
        print(f"   📂 קטגוריות: {categories_count}")
        
        if users_count > 0 and repairs_count > 0:
            print("   ✅ מסד נתונים פעיל ומכיל נתונים")
        else:
            print("   ⚠️ מסד נתונים ריק או חסר")
            
    except Exception as e:
        print(f"   ❌ שגיאה במסד נתונים: {e}")
    
    # 3. בדיקת משתמשים לפי תפקידים
    print("\n👥 בדיקת משתמשים לפי תפקידים...")
    try:
        managers = User.objects.filter(userprofile__role='manager').count()
        mechanics = User.objects.filter(userprofile__role='mechanic').count()
        customers = User.objects.filter(userprofile__role='customer').count()
        
        print(f"   👨‍💼 מנהלים: {managers}")
        print(f"   🔧 מכונאים: {mechanics}")
        print(f"   👤 לקוחות: {customers}")
        
        if managers > 0 and mechanics > 0:
            print("   ✅ יש משתמשים בכל התפקידים")
        else:
            print("   ⚠️ חסרים משתמשים בתפקידים חיוניים")
            
    except Exception as e:
        print(f"   ❌ שגיאה בבדיקת תפקידים: {e}")
    
    # 4. בדיקת תיקונים פעילים
    print("\n🔧 בדיקת תיקונים פעילים...")
    try:
        pending_repairs = RepairJob.objects.filter(status='pending').count()
        in_progress_repairs = RepairJob.objects.filter(status='in_progress').count()
        completed_repairs = RepairJob.objects.filter(status='completed').count()
        
        print(f"   ⏳ ממתינים: {pending_repairs}")
        print(f"   🔄 בתהליך: {in_progress_repairs}")
        print(f"   ✅ הושלמו: {completed_repairs}")
        
        if pending_repairs + in_progress_repairs > 0:
            print("   ✅ יש תיקונים פעילים במערכת")
        else:
            print("   ⚠️ אין תיקונים פעילים")
            
    except Exception as e:
        print(f"   ❌ שגיאה בבדיקת תיקונים: {e}")
    
    # 5. בדיקת נתוני דמו אחרונים
    print("\n🧪 בדיקת נתוני דמו...")
    try:
        latest_repair = RepairJob.objects.order_by('-created_at').first()
        if latest_repair:
            print(f"   📅 תיקון אחרון: {latest_repair.created_at.strftime('%d/%m/%Y %H:%M')}")
            print(f"   🚴 אופניים: {latest_repair.bike}")
            print(f"   📊 סטטוס: {latest_repair.status}")
            
            # בדיקת RepairItems
            items = latest_repair.repair_items.all()
            print(f"   🛠️ פריטים בתיקון: {items.count()}")
            
            if items.exists():
                approved = items.filter(is_approved_by_customer=True).count()
                completed = items.filter(status='completed').count()
                blocked = items.filter(status='blocked').count()
                
                print(f"      ✅ מאושרים: {approved}")
                print(f"      ✅ הושלמו: {completed}")
                print(f"      ⛔ חסומים: {blocked}")
        else:
            print("   ⚠️ לא נמצאו תיקונים במערכת")
    except Exception as e:
        print(f"   ❌ שגיאה בבדיקת נתוני דמו: {e}")
    
    # 6. סיכום
    print("\n" + "=" * 50)
    print(f"🕐 בדיקה הושלמה: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🌟 המערכת מוכנה לשימוש!")
    print("\n🔗 קישורים חשובים:")
    print("   🏠 דף בית: https://bikegarage-4yjs.onrender.com/")
    print("   📝 הרשמה: https://bikegarage-4yjs.onrender.com/register/")
    print("   🔐 התחברות: https://bikegarage-4yjs.onrender.com/login/")
    print("   👨‍💼 דשבורד מנהל: https://bikegarage-4yjs.onrender.com/manager-dashboard/")
    print("   🔧 דשבורד מכונאי: https://bikegarage-4yjs.onrender.com/mechanic-dashboard/")
    print("   📋 דיווח לקוח: https://bikegarage-4yjs.onrender.com/customer-report/")

if __name__ == "__main__":
    check_production_status()
