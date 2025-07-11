#!/usr/bin/env python
"""
סקריפט התחלת עבודה - מכין את הסביבה לפיתוח
"""

import subprocess
import sys
import os

def run_command(command, description):
    """הרצת פקודה עם תיאור"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - הושלם")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - שגיאה: {e}")
        return False

def start_development():
    """התחלת סביבת פיתוח"""
    print("🚀 התחלת סביבת פיתוח מוסך האופניים")
    print("=" * 50)
    
    # בדיקת תיקיית עבודה
    if not os.path.exists("manage.py"):
        print("❌ לא נמצא manage.py - ודא שאתה בתיקיית הפרויקט הנכונה")
        return False
    
    print("✅ נמצא בתיקיית הפרויקט")
    
    # עדכון מgit
    print("\n📥 עדכון מ-Git...")
    if run_command("git pull origin main", "משיכת עדכונים מGit"):
        print("✅ הפרויקט מעודכן")
    
    # בדיקת virtual environment
    if os.path.exists("venv"):
        print("✅ Virtual environment קיים")
    else:
        print("⚠️ Virtual environment לא נמצא")
        print("צור אחד עם: python -m venv venv")
    
    # הרצת migrations
    print("\n🔄 הרצת Migrations...")
    run_command("python manage.py migrate", "הרצת migrations")
    
    # בדיקת תקינות
    print("\n🔍 בדיקת תקינות המערכת...")
    run_command("python check_production_errors.py", "בדיקת תקינות")
    
    print("\n" + "=" * 50)
    print("🎉 סביבת הפיתוח מוכנה!")
    print("\nלהתחלת עבודה:")
    print("1. python manage.py runserver")
    print("2. לך לדפדפן: http://127.0.0.1:8000/")
    print("\nלפני Push:")
    print("python pre_push_check.py")
    
    print("\n📋 פרטי התחברות (משתמשי דמו):")
    print("Admin: admin / admin123")
    print("Manager: manager1 / manager123")
    print("Mechanic: mechanic1 / mechanic123")
    print("Customer: customer1 / customer123")
    
    return True

if __name__ == "__main__":
    success = start_development()
    if success:
        print("\n🚀 הכל מוכן! התחל לעבוד...")
    else:
        print("\n❌ יש בעיות בהתחלת העבודה")
    
    sys.exit(0 if success else 1)
