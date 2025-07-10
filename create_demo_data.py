#!/usr/bin/env python3
"""
יצירת נתוני דמו מהירה לבדיקת אקורדיון
"""

import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def create_demo_data():
    from workshop.models import RepairCategory, RepairSubCategory, Customer, Bike
    from django.contrib.auth.models import User
    
    print("🔧 יצירת נתוני דמו לבדיקת אקורדיון...")
    
    # קטגוריות ותת-קטגוריות מפורטות
    categories_data = {
        'בלמים': [
            'בלמים לא עוצרים כראוי',
            'חריקות בלמים', 
            'ידיות בלמים רפויות',
            'דיסקים מעוותים',
            'רפידות בלמים שחוקות'
        ],
        'גלגלים': [
            'פנצ\'ר בגלגל',
            'גלגל עקום',
            'חישוקים שבורים',
            'חוטי חישוק שבורים',
            'מסבי גלגלים שחוקים'
        ],
        'שרשרת וגירים': [
            'שרשרת קופצת',
            'שרשרת חורקת',
            'שרשרת שבורה',
            'מעביר אחורי לא פועל',
            'מעביר קדמי לא פועל'
        ],
        'כידון ובקרה': [
            'כידון רופף',
            'הגה לא נסגר',
            'מסבי כידון שחוקים',
            'ידיות שחוקות'
        ]
    }
    
    total_cats = 0
    total_subcats = 0
    
    for cat_name, subcats in categories_data.items():
        category, created = RepairCategory.objects.get_or_create(name=cat_name)
        if created:
            print(f"✅ נוצרה קטגוריה: {cat_name}")
            total_cats += 1
        
        for sub_name in subcats:
            subcat, created = RepairSubCategory.objects.get_or_create(
                category=category,
                name=sub_name
            )
            if created:
                print(f"  ✅ נוצרה תת-קטגוריה: {sub_name}")
                total_subcats += 1
    
    # יצירת משתמש דמו אם לא קיים
    demo_user, user_created = User.objects.get_or_create(
        username="demo_customer",
        defaults={
            'first_name': 'לקוח',
            'last_name': 'דמו',
            'email': 'demo@example.com'
        }
    )
    if user_created:
        demo_user.set_password('demo123')
        demo_user.save()
        print(f"✅ נוצר משתמש דמו: {demo_user.username}")
    
    # לקוח ואופניים לדמו
    customer, created = Customer.objects.get_or_create(
        user=demo_user,
        defaults={
            'name': "לקוח דמו",
            'phone': '050-1234567',
            'email': 'demo@example.com'
        }
    )
    if created:
        print(f"✅ נוצר לקוח: {customer.name}")
    
    bikes_data = [
        {'brand': 'Trek', 'model': 'X-Caliber', 'color': 'כחול'},
        {'brand': 'Giant', 'model': 'Talon', 'color': 'אדום'},
    ]
    
    for bike_data in bikes_data:
        bike, created = Bike.objects.get_or_create(
            customer=customer,
            brand=bike_data['brand'],
            defaults=bike_data
        )
        if created:
            print(f"✅ נוצרו אופניים: {bike}")
    
    print(f"\n📊 סיכום נתוני דמו:")
    print(f"   קטגוריות: {RepairCategory.objects.count()} (חדשות: {total_cats})")
    print(f"   תת-קטגוריות: {RepairSubCategory.objects.count()} (חדשות: {total_subcats})")
    print(f"   לקוחות: {Customer.objects.count()}")
    print(f"   אופניים: {Bike.objects.count()}")
    
    print(f"\n🎯 פרטי כניסה לבדיקה:")
    print(f"   משתמש: demo_customer")
    print(f"   סיסמה: demo123")
    print(f"   URL: http://localhost:8000/customer/report/")

def print_current_data():
    """הצגת נתונים נוכחיים"""
    from workshop.models import RepairCategory, RepairSubCategory
    
    print(f"\n🔍 נתונים נוכחיים במערכת:")
    print(f"   קטגוריות: {RepairCategory.objects.count()}")
    print(f"   תת-קטגוריות: {RepairSubCategory.objects.count()}")
    
    if RepairSubCategory.objects.exists():
        print(f"\n📋 תת-קטגוריות (דוגמאות):")
        for subcat in RepairSubCategory.objects.select_related('category')[:10]:
            print(f"   - {subcat}")

if __name__ == "__main__":
    print_current_data()
    create_demo_data()
    print_current_data()
