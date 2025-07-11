#!/usr/bin/env python
"""
סקריפט בדיקה לפני Push לproduction
"""

import subprocess
import sys
import os

def run_command(command, description):
    """הרצת פקודה עם תיאור"""
    print(f"\n📋 {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            if result.stdout.strip():
                print(f"   📄 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"   🚨 {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def check_git_status():
    """בדיקת מצב git"""
    print("\n🔍 בדיקת מצב Git...")
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    
    if result.stdout.strip():
        print("📝 קבצים שישונו:")
        for line in result.stdout.strip().split('\n'):
            print(f"   {line}")
        return True
    else:
        print("✅ אין שינויים חדשים")
        return False

def pre_push_check():
    """בדיקה מקיפה לפני push"""
    print("🚀 בדיקה לפני Push לProduction")
    print("=" * 50)
    
    # בדיקת שינויים
    has_changes = check_git_status()
    if not has_changes:
        print("\n⚠️ אין שינויים לpush")
        return True
    
    checks = [
        ("python check_production_errors.py", "בדיקת תקינות כללית"),
        ("python manage.py check", "בדיקת Django"),
        ("python manage.py makemigrations --dry-run", "בדיקת migrations חדשים"),
        ("python manage.py collectstatic --dry-run --noinput", "בדיקת static files"),
    ]
    
    all_passed = True
    
    for command, description in checks:
        if not run_command(command, description):
            all_passed = False
    
    # בדיקת requirements.txt
    if os.path.exists("requirements.txt"):
        print("\n📋 בדיקת requirements.txt...")
        print("✅ requirements.txt קיים")
    else:
        print("\n⚠️ requirements.txt לא נמצא")
    
    # בדיקת Procfile
    if os.path.exists("Procfile"):
        print("✅ Procfile קיים")
    else:
        print("⚠️ Procfile לא נמצא")
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 כל הבדיקות עברו - מוכן לPush!")
        print("\nלהמשך deployment:")
        print("git add .")
        print('git commit -m "תיאור השינוי"')
        print("git push origin main")
        print("\nאחרי Push בדוק:")
        print("https://shai-bike-garage.onrender.com/")
        return True
    else:
        print("⚠️ יש בעיות שיש לתקן לפני Push!")
        print("תקן את השגיאות ונסה שוב.")
        return False

if __name__ == "__main__":
    success = pre_push_check()
    sys.exit(0 if success else 1)
