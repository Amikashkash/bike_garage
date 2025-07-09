#!/usr/bin/env python3
"""
סקריפט לבדיקת תיקוני JavaScript ו-manifest
נוצר: דצמבר 2024
"""

import os
import re
import sys

def test_manifest_syntax():
    """בדיקת syntax של manifest.json"""
    print("🔍 בודק syntax של manifest.json...")
    
    base_html_path = "workshop/templates/workshop/base.html"
    if not os.path.exists(base_html_path):
        print("❌ קובץ base.html לא נמצא")
        return False
    
    with open(base_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # חיפוש manifest
    manifest_match = re.search(r'href="data:application/json,([^"]+)"', content)
    if not manifest_match:
        print("❌ לא נמצא manifest.json")
        return False
    
    manifest_content = manifest_match.group(1)
    
    # בדיקה שאין apostrophes בלתי מוגנים
    if "'" in manifest_content and "&quot;" not in manifest_content:
        print("❌ נמצאו apostrophes לא מוגנים ב-manifest")
        return False
    
    print("✅ manifest.json נראה תקין")
    return True

def test_javascript_safety():
    """בדיקת הקוד JavaScript לאבטחת שגיאות"""
    print("🔍 בודק קוד JavaScript...")
    
    report_html_path = "workshop/templates/workshop/customer_report.html"
    if not os.path.exists(report_html_path):
        print("❌ קובץ customer_report.html לא נמצא")
        return False
    
    with open(report_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # בדיקות בטיחות
    checks = [
        ("Array.from בטוח", r"subcategoriesSelect && subcategoriesSelect\.options"),
        ("בדיקת אלמנטים", r"if \(!subcategoriesSelect\)"),
        ("בדיקת accordion", r"if \(!accordionContainer\)"),
        ("בדיקת fallback", r"if \(!fallbackContainer\)"),
        ("סנכרון בטוח", r"if \(subcategoriesSelect && subcategoriesSelect\.options\)")
    ]
    
    all_passed = True
    for check_name, pattern in checks:
        if re.search(pattern, content):
            print(f"✅ {check_name}")
        else:
            print(f"❌ חסר: {check_name}")
            all_passed = False
    
    return all_passed

def test_console_errors():
    """יצירת הוראות לבדיקת שגיאות קונסול"""
    print("\n📋 הוראות לבדיקת קונסול:")
    print("1. הפעל את השרת")
    print("2. פתח את דף דיווח התקלה")
    print("3. פתח Developer Tools (F12)")
    print("4. בדוק שאין שגיאות בקונסול")
    print("5. נסה את האקורדיון")

def main():
    """הפעלה ראשית"""
    print("🧪 בדיקת תיקוני JavaScript ו-manifest")
    print("=" * 50)
    
    manifest_ok = test_manifest_syntax()
    js_ok = test_javascript_safety()
    
    print("\n📊 תוצאות:")
    print(f"Manifest: {'✅ תקין' if manifest_ok else '❌ בעייתי'}")
    print(f"JavaScript: {'✅ בטוח' if js_ok else '❌ בעייתי'}")
    
    if manifest_ok and js_ok:
        print("\n🎉 כל התיקונים עברו בהצלחה!")
        test_console_errors()
        return True
    else:
        print("\n⚠️ יש בעיות שדורשות תיקון")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
