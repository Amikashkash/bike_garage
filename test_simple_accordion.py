#!/usr/bin/env python3
"""
בדיקה מהירה של התיקון החדש - פתרון פשוט לאקורדיון
נוצר: דצמבר 2024
"""

import re

def test_simple_accordion():
    """בדיקת הקוד החדש הפשוט"""
    print("🔍 בודק קוד JavaScript מפושט...")
    
    with open("workshop/templates/workshop/customer_report.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ("חיפוש checkboxes פשוט", r'querySelectorAll\(\'input\[type="checkbox"\]\[name="subcategories"\]\'\)'),
        ("לוג מספר checkboxes", r'console\.log\(`Found \${checkboxes\.length}'),
        ("פונקציית toggleAccordion", r'function toggleAccordion\(categoryId\)'),
        ("פונקציית syncCheckbox", r'function syncCheckbox\(value, checked\)'),
        ("בניית HTML באמצעות string", r'accordionHTML \+= `'),
        ("סנכרון עם טופס מקורי", r'originalCheckbox\.checked = checked'),
        ("הסתרת fallback", r'fallbackContainer\.style\.display = \'none\'')
    ]
    
    all_passed = True
    for check_name, pattern in checks:
        if re.search(pattern, content):
            print(f"✅ {check_name}")
        else:
            print(f"❌ חסר: {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """הפעלה ראשית"""
    print("🧪 בדיקת פתרון פשוט לאקורדיון")
    print("=" * 40)
    
    if test_simple_accordion():
        print("\n✅ הקוד החדש נראה תקין!")
        print("\n🎯 מה שהקוד עושה:")
        print("1. מחפש checkboxes עם name='subcategories'")
        print("2. מארגן אותם לפי קטגוריות (מפריד ב-' > ')")
        print("3. בונה HTML של אקורדיון")
        print("4. מסתיר את הטופס המקורי")
        print("5. מסנכרן בחירות עם הטופס המקורי")
        print("\n📋 לבדיקה:")
        print("1. הפעל שרת: python manage.py runserver")
        print("2. גש לדיווח תקלה")
        print("3. צפוי לראות אקורדיון עם קטגוריות")
    else:
        print("\n❌ יש בעיות בקוד")

if __name__ == "__main__":
    main()
