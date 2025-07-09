#!/usr/bin/env python3
"""
🧪 סקריפט פשוט ליצירת קטגוריה אחת לבדיקה
"""

import os
import sys
import django

# הוספת נתיב הפרויקט
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def create_basic_categories():
    from workshop.models import RepairCategory, RepairSubCategory
    
    # קטגוריה בסיסית
    category, created = RepairCategory.objects.get_or_create(name='בלמים')
    if created:
        print("✅ נוצרה קטגוריית 'בלמים'")
    
    subcategories = [
        'בלמים לא עוצרים',
        'חריקות בלמים',
        'ידיות בלמים רפויות'
    ]
    
    for sub_name in subcategories:
        sub, created = RepairSubCategory.objects.get_or_create(
            category=category,
            name=sub_name
        )
        if created:
            print(f"✅ נוצרה תת קטגוריה: {sub_name}")
    
    print(f"📊 סה\"כ: {RepairCategory.objects.count()} קטגוריות, {RepairSubCategory.objects.count()} תת קטגוריות")

if __name__ == "__main__":
    create_basic_categories()
