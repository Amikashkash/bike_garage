#!/usr/bin/env python3
"""
בדיקת תיקון האקורדיון עם CheckboxSelectMultiple
נוצר: דצמבר 2024
"""

import os
import re

def test_checkbox_accordion_fix():
    """בדיקת התיקון החדש לאקורדיון"""
    print("🔍 בודק תיקון האקורדיון עם CheckboxSelectMultiple...")
    
    report_html_path = "workshop/templates/workshop/customer_report.html"
    if not os.path.exists(report_html_path):
        print("❌ קובץ customer_report.html לא נמצא")
        return False
    
    with open(report_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # בדיקות התיקון החדש
    checks = [
        ("חיפוש checkboxes", r"querySelectorAll\('input\[type=\"checkbox\"\]'\)"),
        ("בדיקת מספר checkboxes", r"Found \${subcategoryCheckboxes\.length} subcategory checkboxes"),
        ("גישה ל-label", r"checkbox\.parentElement\.querySelector\('label'\)"),
        ("סנכרון דו-כיווני", r"subcategory\.checkbox\.addEventListener\('change'"),
        ("שמירת שם טופס", r"checkbox\.name = subcategory\.checkbox\.name"),
        ("הסרת הפניה ל-subcategoriesSelect", "subcategoriesSelect")
    ]
    
    all_passed = True
    for check_name, pattern in checks:
        if check_name == "הסרת הפניה ל-subcategoriesSelect":
            # זה צריך לא להימצא
            if pattern not in content:
                print(f"✅ {check_name}")
            else:
                print(f"❌ עדיין יש הפניה ל-subcategoriesSelect")
                all_passed = False
        else:
            if re.search(pattern, content):
                print(f"✅ {check_name}")
            else:
                print(f"❌ חסר: {check_name}")
                all_passed = False
    
    return all_passed

def test_form_widget():
    """בדיקת הטופס להשתמש ב-CheckboxSelectMultiple"""
    print("\n🔍 בודק הגדרת widget בטופס...")
    
    forms_path = "workshop/forms.py"
    if not os.path.exists(forms_path):
        print("❌ קובץ forms.py לא נמצא")
        return False
    
    with open(forms_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "CheckboxSelectMultiple" in content:
        print("✅ הטופס משתמש ב-CheckboxSelectMultiple")
        return True
    else:
        print("❌ הטופס לא משתמש ב-CheckboxSelectMultiple")
        return False

def main():
    """הפעלה ראשית"""
    print("🧪 בדיקת תיקון האקורדיון")
    print("=" * 40)
    
    accordion_ok = test_checkbox_accordion_fix()
    form_ok = test_form_widget()
    
    print("\n📊 תוצאות:")
    print(f"תיקון אקורדיון: {'✅ תקין' if accordion_ok else '❌ בעייתי'}")
    print(f"הגדרת טופס: {'✅ תקין' if form_ok else '❌ בעייתי'}")
    
    if accordion_ok and form_ok:
        print("\n🎉 התיקון הושלם בהצלחה!")
        print("\n📋 מה שצריך לקרות עכשיו:")
        print("1. הטופס המקורי (fallbackCategories) יוסתר")
        print("2. האקורדיון יוצג עם קטגוריות מאורגנות")
        print("3. לא תהיה כפילות של checkboxes")
        print("4. הסנכרון יעבוד דו-כיווני")
        return True
    else:
        print("\n⚠️ יש בעיות שדורשות תיקון")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
