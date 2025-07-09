#!/usr/bin/env python3
"""
🔧 יצירת קטגוריות תקלה לדוגמה
"""

import os
import sys
import django

# הוספת נתיב הפרויקט
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairCategory, RepairSubCategory

def create_sample_categories():
    """יצירת קטגוריות תקלה לדוגמה"""
    
    print("🔧 יוצר קטגוריות תקלה לדוגמה...")
    
    categories_data = {
        'בלמים': [
            'בלמים לא עוצרים',
            'חריקות בלמים',
            'ידיות בלמים רפויות',
            'דיסקים מעוותים',
            'רפידות בלמים בלויות'
        ],
        'הילוכים': [
            'הילוכים לא מתחלפים',
            'שרשרת קופצת',
            'קלת הילוכים לא עובדת',
            'דראייר פגום',
            'כבל הילוכים תקוע'
        ],
        'גלגלים וצמיגים': [
            'צמיג פנצ\'ר',
            'חישוק עקום',
            'ספוקים שבורים',
            'מיסבים פגומים',
            'אוויר בגלגל נגמר'
        ],
        'מערכת הנעה': [
            'דוושות רפויות',
            'שרשרת שבורה',
            'גלגל שיניים בלוי',
            'תושבת תנועה רפויה',
            'שרשרת מחליקה'
        ],
        'מסגרת וכידון': [
            'מסגרת סדוקה',
            'כידון רפוי',
            'מושב לא יציב',
            'גובה אוכף לא נכון',
            'צינור כידון תקוע'
        ]
    }
    
    created_categories = 0
    created_subcategories = 0
    
    for cat_name, subcats in categories_data.items():
        category, created = RepairCategory.objects.get_or_create(name=cat_name)
        if created:
            created_categories += 1
            print(f"✅ נוצרה קטגוריה: {cat_name}")
        else:
            print(f"📁 קטגוריה קיימת: {cat_name}")
        
        for subcat_name in subcats:
            subcat, created = RepairSubCategory.objects.get_or_create(
                category=category,
                name=subcat_name
            )
            if created:
                created_subcategories += 1
                print(f"  ✅ נוצרה תת קטגוריה: {subcat_name}")
    
    print(f"\n🎉 סיכום:")
    print(f"📁 קטגוריות חדשות: {created_categories}")
    print(f"📂 תתי קטגוריות חדשות: {created_subcategories}")
    
    # סיכום כולל
    total_categories = RepairCategory.objects.count()
    total_subcategories = RepairSubCategory.objects.count()
    print(f"\n📊 סה\"כ במערכת:")
    print(f"📁 קטגוריות: {total_categories}")
    print(f"📂 תתי קטגוריות: {total_subcategories}")
    
    return total_categories > 0

def main():
    print("🧪 בודק קטגוריות תקלה במערכת...")
    
    # בדיקת מצב נוכחי
    categories_count = RepairCategory.objects.count()
    subcategories_count = RepairSubCategory.objects.count()
    
    print(f"📁 קטגוריות נוכחיות: {categories_count}")
    print(f"📂 תתי קטגוריות נוכחיות: {subcategories_count}")
    
    if categories_count == 0:
        print("\n⚠️  אין קטגוריות במערכת!")
        print("💡 אני יוצר קטגוריות לדוגמה...")
        success = create_sample_categories()
        
        if success:
            print("\n🎯 עכשיו אפשר לבדוק:")
            print("1. python manage.py runserver")
            print("2. התחבר כלקוח")
            print("3. לך ל-/customer/report/")
            print("4. ראה את האקורדיון החדש!")
    else:
        print("✅ יש קטגוריות במערכת")
        
        # הצגת הקטגוריות הקיימות
        for category in RepairCategory.objects.all():
            subcats = category.subcategories.all()
            print(f"📁 {category.name} ({subcats.count()} תתי קטגוריות)")
            for subcat in subcats:
                print(f"  📂 {subcat.name}")

if __name__ == "__main__":
    main()
