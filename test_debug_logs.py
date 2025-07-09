#!/usr/bin/env python3
"""
בדיקה מהירה של התיקונים החדשים
נוצר: דצמבר 2024
"""

import re

def test_javascript_debug():
    """בדיקת הוספת debug logs"""
    print("🔍 בודק debug logs בקוד JavaScript...")
    
    with open("workshop/templates/workshop/customer_report.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    debug_checks = [
        ("לוג fallbackContainer", r"console\.log\('Looking for checkboxes in fallbackContainer:'"),
        ("לוג HTML content", r"console\.log\('fallbackContainer HTML:'"),
        ("לוג כל checkboxes", r"console\.log\(`Found \${allCheckboxes\.length} checkboxes"),
        ("לוג processing", r"console\.log\(`Processing:"),
        ("ניקוי HTML entities", r"replace\(/&gt;/g, '>'\)"),
        ("לוג categories found", r"console\.log\('Categories found:'"),
        ("לוג categories data", r"console\.log\('Categories data:'")
    ]
    
    all_passed = True
    for check_name, pattern in debug_checks:
        if re.search(pattern, content):
            print(f"✅ {check_name}")
        else:
            print(f"❌ חסר: {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """הפעלה ראשית"""
    print("🧪 בדיקת debug logs")
    print("=" * 30)
    
    if test_javascript_debug():
        print("\n✅ כל ה-debug logs נוספו!")
        print("\n📋 כדי לבדוק:")
        print("1. הפעל את השרת")
        print("2. התחבר כלקוח ולך לדיווח תקלה")
        print("3. פתח F12 -> Console")
        print("4. רענן את הדף")
        print("5. בדוק את הלוגים")
    else:
        print("\n❌ חסרים debug logs")

if __name__ == "__main__":
    main()
