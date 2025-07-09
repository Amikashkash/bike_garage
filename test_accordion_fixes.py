#!/usr/bin/env python3
"""
בדיקה מהירה של תיקוני האקורדיון והmanifest
נוצר: דצמבר 2024
"""

import os
import sys

def test_manifest_file():
    """בדיקת קובץ manifest.json"""
    print("🔍 בודק קובץ manifest.json...")
    
    manifest_path = "workshop/static/workshop/manifest.json"
    if not os.path.exists(manifest_path):
        print("❌ קובץ manifest.json לא נמצא")
        return False
    
    try:
        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
        
        required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
        for field in required_fields:
            if field in manifest_data:
                print(f"✅ {field}: {manifest_data[field]}")
            else:
                print(f"❌ חסר שדה: {field}")
                return False
        
        print("✅ manifest.json תקין!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ שגיאת JSON: {e}")
        return False

def test_accordion_logic():
    """בדיקת לוגיקת האקורדיון"""
    print("\n🔍 בודק לוגיקת האקורדיון...")
    
    report_html_path = "workshop/templates/workshop/customer_report.html"
    if not os.path.exists(report_html_path):
        print("❌ קובץ customer_report.html לא נמצא")
        return False
    
    with open(report_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # בדיקות לוגיקה
    checks = [
        ("בדיקת value לא ריק", r"option\.value && option\.value\.trim\(\) !== ''"),
        ("לוג מספר קטגוריות", r"console\.log\(`Found \${availableOptions\.length}"),
        ("הסתרת fallback", r"fallbackContainer\.style\.display = 'none'"),
        ("הודעה על בניית אקורדיון", r"console\.log\('Building accordion with categories'\)")
    ]
    
    all_passed = True
    for check_name, pattern in checks:
        import re
        if re.search(pattern, content):
            print(f"✅ {check_name}")
        else:
            print(f"❌ חסר: {check_name}")
            all_passed = False
    
    return all_passed

def test_settings_static():
    """בדיקת הגדרות static files"""
    print("\n🔍 בודק הגדרות static files...")
    
    settings_path = "garage/settings.py"
    if not os.path.exists(settings_path):
        print("❌ קובץ settings.py לא נמצא")
        return False
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'STATICFILES_DIRS' in content:
        print("✅ STATICFILES_DIRS מוגדר")
        return True
    else:
        print("❌ STATICFILES_DIRS לא מוגדר")
        return False

def main():
    """הפעלה ראשית"""
    print("🧪 בדיקת תיקוני אקורדיון ו-manifest")
    print("=" * 50)
    
    tests = [
        ("קובץ manifest.json", test_manifest_file),
        ("לוגיקת אקורדיון", test_accordion_logic),
        ("הגדרות static", test_settings_static)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("📊 תוצאות סיכום:")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ עבר" if result else "❌ נכשל"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 כל התיקונים מוכנים!")
        print("\n📋 הוראות בדיקה:")
        print("1. הפעל: python manage.py runserver")
        print("2. גש לדף דיווח תקלה")
        print("3. בדוק שהאקורדיון מוצג נכון")
        print("4. בדוק שאין שגיאות בקונסול")
        print("5. בדוק שה-manifest עובד (F12 > Application > Manifest)")
    else:
        print("\n⚠️ יש בעיות שדורשות תיקון")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
