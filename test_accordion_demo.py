#!/usr/bin/env python3
"""
בדיקה מלאה של אקורדיון התקלות
"""

import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def ensure_test_data():
    """יצירת נתוני דמו לבדיקה"""
    from workshop.models import RepairCategory, RepairSubCategory, Customer, Bike
    from django.contrib.auth.models import User
    
    print("🔧 יצירת נתוני דמו...")
    
    # קטגוריות ותת-קטגוריות
    categories_data = {
        'בלמים': [
            'בלמים לא עוצרים',
            'חריקות בלמים', 
            'ידיות בלמים רפויות'
        ],
        'גלגלים': [
            'פנצ\'ר', 
            'גלגל עקום',
            'חישוקים שבורים'
        ],
        'שרשרת': [
            'שרשרת קופצת',
            'שרשרת חורקת',
            'שרשרת שבורה'
        ]
    }
    
    for cat_name, subcats in categories_data.items():
        category, created = RepairCategory.objects.get_or_create(name=cat_name)
        if created:
            print(f"✅ נוצרה קטגוריה: {cat_name}")
        
        for sub_name in subcats:
            subcat, created = RepairSubCategory.objects.get_or_create(
                category=category,
                name=sub_name
            )
            if created:
                print(f"  ✅ נוצרה תת-קטגוריה: {sub_name}")
    
    # לקוח ואופניים לדמו
    customer, created = Customer.objects.get_or_create(
        name="יוסי כהן",
        defaults={'phone': '050-1234567', 'email': 'yossi@example.com'}
    )
    if created:
        print(f"✅ נוצר לקוח: {customer.name}")
    
    bike, created = Bike.objects.get_or_create(
        customer=customer,
        brand="Trek",
        defaults={'model': 'X-Caliber', 'color': 'כחול'}
    )
    if created:
        print(f"✅ נוצרו אופניים: {bike}")
    
    print(f"\n📊 סיכום:")
    print(f"   קטגוריות: {RepairCategory.objects.count()}")
    print(f"   תת-קטגוריות: {RepairSubCategory.objects.count()}")
    print(f"   לקוחות: {Customer.objects.count()}")
    print(f"   אופניים: {Bike.objects.count()}")

def test_form_structure():
    """בדיקת מבנה הטופס"""
    from workshop.forms import CustomerRepairJobForm
    from workshop.models import RepairSubCategory, Bike
    
    print("\n🔍 בדיקת מבנה הטופס...")
    
    form = CustomerRepairJobForm()
    
    # בדיקת queryset של subcategories
    subcats = form.fields['subcategories'].queryset
    print(f"תת-קטגוריות זמינות: {subcats.count()}")
    
    for subcat in subcats[:10]:  # הצגת 10 הראשונות
        print(f"  - {subcat.category.name} > {subcat.name}")
    
    # בדיקת אופניים זמינים
    bikes = Bike.objects.all()
    print(f"אופניים זמינים: {bikes.count()}")
    for bike in bikes[:5]:
        print(f"  - {bike}")

def check_template_structure():
    """בדיקת מבנה התבנית"""
    print("\n🔍 בדיקת מבנה התבנית...")
    
    try:
        with open('workshop/templates/workshop/customer_report.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # בדיקות בסיסיות
        checks = [
            ('id="categoriesAccordion"', 'מקום לאקורדיון'),
            ('id="fallbackCategories"', 'מקום לטופס גיבוי'),
            ('function toggleAccordion', 'פונקציית אקורדיון'),
            ('function syncCheckbox', 'פונקציית סנכרון'),
            ('subcategories', 'שדה תת-קטגוריות'),
            ('form.subcategories', 'רינדור שדה Django')
        ]
        
        for check, desc in checks:
            if check in content:
                print(f"  ✅ {desc}")
            else:
                print(f"  ❌ חסר: {desc}")
                
    except FileNotFoundError:
        print("  ❌ קובץ התבנית לא נמצא")

def main():
    print("🧪 בדיקה מלאה של אקורדיון התקלות")
    print("=" * 50)
    
    ensure_test_data()
    test_form_structure()
    check_template_structure()
    
    print("\n🎯 צעדים לבדיקה ידנית:")
    print("1. הפעל שרת: python manage.py runserver")
    print("2. היכנס ל: http://localhost:8000/customer/report/")
    print("3. בדוק שמוצג אקורדיון עם קטגוריות")
    print("4. בדוק שהצ'קבוקסים עובדים")
    print("5. בדוק שהשליחה עובדת")
    
    print("\n🔍 דברים לבדוק:")
    print("- האם מוצג אקורדיון במקום רשימת צ'קבוקסים רגילה?")
    print("- האם לחיצה על כותרת קטגוריה פותחת/סוגרת?")
    print("- האם בחירת צ'קבוקס מסנכרנת עם הטופס?")
    print("- האם זה עובד במובייל?")

if __name__ == "__main__":
    main()
