#!/usr/bin/env python3
"""
בדיקה מהירה של כל הפונקציונליות לאחר תיקוני JavaScript
נוצר: דצמבר 2024
"""

import os
import django
import sys

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import Customer, Bike, RepairJob, RepairCategory, RepairSubCategory
from django.contrib.auth.models import User

def test_database_status():
    """בדיקת מצב הנתונים"""
    print("🗄️ בודק מצב הנתונים...")
    
    customers = Customer.objects.count()
    bikes = Bike.objects.count()
    categories = RepairCategory.objects.count()
    subcategories = RepairSubCategory.objects.count()
    repair_jobs = RepairJob.objects.count()
    
    print(f"👥 לקוחות: {customers}")
    print(f"🚲 אופניים: {bikes}")
    print(f"📁 קטגוריות: {categories}")
    print(f"📋 תת קטגוריות: {subcategories}")
    print(f"🔧 תיקונים: {repair_jobs}")
    
    if categories == 0:
        print("⚠️ אין קטגוריות - האקורדיון יציג הודעת fallback")
    else:
        print("✅ יש קטגוריות - האקורדיון יעבוד")
    
    return True

def test_template_files():
    """בדיקת קיום קבצי תבניות"""
    print("\n📄 בודק קבצי תבניות...")
    
    templates = [
        "workshop/templates/workshop/base.html",
        "workshop/templates/workshop/customer_report.html",
        "workshop/templates/workshop/customer_list.html",
        "workshop/templates/workshop/customer_with_bike_form.html",
        "workshop/templates/workshop/customer_add_bike.html",
        "workshop/templates/workshop/customer_bikes_list.html"
    ]
    
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {os.path.basename(template)}")
        else:
            print(f"❌ {os.path.basename(template)} לא נמצא")
            all_exist = False
    
    return all_exist

def test_url_patterns():
    """בדיקת תקינות URL patterns"""
    print("\n🔗 בודק URL patterns...")
    
    try:
        from django.urls import reverse
        
        urls_to_test = [
            'customer_list',
            'customer_add_bike',
            'customer_bikes_list',
            'customer_with_bike_new',
            'customer_report',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name}: {url}")
            except Exception as e:
                print(f"❌ {url_name}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקת URLs: {e}")
        return False

def test_form_fields():
    """בדיקת שדות בטפסים"""
    print("\n📝 בודק טפסים...")
    
    try:
        from workshop.forms import CustomerRegisterForm, CustomerRepairJobForm
        
        # בדיקת CustomerRegisterForm
        form = CustomerRegisterForm()
        bike_fields = ['bike_model', 'bike_brand', 'bike_color', 'has_bike']
        
        for field in bike_fields:
            if field in form.fields:
                print(f"✅ {field} קיים ב-CustomerRegisterForm")
            else:
                print(f"❌ {field} חסר ב-CustomerRegisterForm")
                return False
        
        # בדיקת CustomerRepairJobForm
        repair_form = CustomerRepairJobForm()
        if 'subcategories' in repair_form.fields:
            print("✅ subcategories קיים ב-CustomerRepairJobForm")
        else:
            print("❌ subcategories חסר ב-CustomerRepairJobForm")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקת טפסים: {e}")
        return False

def create_test_scenario():
    """יצירת תרחיש בדיקה"""
    print("\n🧪 יוצר תרחיש בדיקה...")
    
    try:
        # יצירת משתמש בדיקה אם לא קיים
        if not User.objects.filter(username='test_customer').exists():
            user = User.objects.create_user(
                username='test_customer',
                email='test@example.com',
                password='testpass123',
                first_name='לקוח',
                last_name='בדיקה'
            )
            
            customer = Customer.objects.create(
                user=user,
                name='לקוח בדיקה',
                phone='050-1234567',
                email='test@example.com'
            )
            
            bike = Bike.objects.create(
                customer=customer,
                model='אופניים לבדיקה',
                brand='מותג בדיקה',
                color='כחול'
            )
            
            print("✅ נוצר לקוח ואופניים לבדיקה")
        else:
            print("✅ לקוח בדיקה כבר קיים")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת תרחיש בדיקה: {e}")
        return False

def main():
    """הפעלה ראשית"""
    print("🔍 בדיקה מהירה של המערכת לאחר תיקוני JavaScript")
    print("=" * 60)
    
    tests = [
        ("מצב נתונים", test_database_status),
        ("קבצי תבניות", test_template_files),
        ("URL patterns", test_url_patterns),
        ("שדות טפסים", test_form_fields),
        ("תרחיש בדיקה", create_test_scenario)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        results[test_name] = test_func()
    
    print("\n" + "=" * 60)
    print("📊 תוצאות סיכום:")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ עבר" if result else "❌ נכשל"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 כל הבדיקות עברו בהצלחה!")
        print("\n📋 הוראות המשך:")
        print("1. הפעל: python manage.py runserver")
        print("2. גש ל: http://localhost:8000")
        print("3. התחבר כלקוח (test_customer / testpass123)")
        print("4. נסה את דף דיווח התקלה")
        print("5. בדוק שאין שגיאות בקונסול (F12)")
    else:
        print("\n⚠️ יש בעיות שדורשות תיקון")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
