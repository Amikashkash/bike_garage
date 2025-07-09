#!/usr/bin/env python3
"""
בדיקת הטופס וה-widget של subcategories
נוצר: דצמבר 2024
"""

import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.forms import CustomerRepairJobForm
from workshop.models import Customer, Bike, RepairSubCategory

def test_form_rendering():
    """בדיקת איך הטופס מתרנדר"""
    print("🔍 בודק רינדור הטופס...")
    
    # יצירת טופס
    form = CustomerRepairJobForm()
    
    # בדיקת השדה subcategories
    subcategories_field = form.fields['subcategories']
    print(f"Widget type: {type(subcategories_field.widget)}")
    print(f"Queryset count: {subcategories_field.queryset.count()}")
    
    # רינדור השדה
    rendered_field = str(form['subcategories'])
    print("\n--- רינדור השדה ---")
    print(rendered_field[:500] + "..." if len(rendered_field) > 500 else rendered_field)
    
    # בדיקת הנתונים
    print(f"\n--- נתונים ---")
    for subcategory in subcategories_field.queryset[:5]:  # רק 5 ראשונים
        print(f"- {subcategory}")
    
    return True

def test_customer_form():
    """בדיקת טופס ללקוח ספציפי"""
    print("\n🔍 בודק טופס עם אופניים...")
    
    try:
        # מציאת לקוח עם אופניים
        customer = Customer.objects.filter(bikes__isnull=False).first()
        if not customer:
            print("❌ לא נמצא לקוח עם אופניים")
            return False
        
        print(f"לקוח: {customer.name}")
        bikes = customer.bikes.all()
        print(f"אופניים: {[str(bike) for bike in bikes]}")
        
        # יצירת טופס
        form = CustomerRepairJobForm()
        form.fields['bike'].queryset = bikes
        
        print(f"אפשרויות אופניים בטופס: {form.fields['bike'].queryset.count()}")
        print(f"אפשרויות תקלות בטופס: {form.fields['subcategories'].queryset.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        return False

def main():
    """הפעלה ראשית"""
    print("🧪 בדיקת טופס דיווח תקלה")
    print("=" * 40)
    
    form_ok = test_form_rendering()
    customer_ok = test_customer_form()
    
    if form_ok and customer_ok:
        print("\n✅ הטופס נראה תקין")
        print("\n💡 אם האקורדיון לא מוצג, בדוק בקונסול הדפדפן")
    else:
        print("\n❌ יש בעיה בטופס")

if __name__ == "__main__":
    main()
