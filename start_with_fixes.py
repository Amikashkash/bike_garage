#!/usr/bin/env python
"""
הפעלת השרת עם התיקונים החדשים
"""

import subprocess
import sys
import os

def restart_server():
    print("🚀 מפעיל שרת עם התיקונים החדשים...")
    
    # עצירת שרתים קיימים
    try:
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True)
        print("⏹️ עצרתי שרתים קיימים")
    except:
        pass
    
    # החזרה לתיקיית הפרויקט
    os.chdir('c:\\bikegarage')
    
    # הפעלת השרת
    print("🌐 מפעיל שרת Django...")
    print("📋 אחרי שהשרת יעלה:")
    print("   1. כנס לדשבורד מנהל: http://localhost:8000/manager/")
    print("   2. התחבר כמנהל (admin_test / admin123)")
    print("   3. בדוק שיש עמודה 'הערות מכונאי' בטבלת 'בביצוע'")
    print("   4. לחץ על כפתור 'פעולות ממתינות' - אמור לעבוד ללא בעיות הרשאות")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
    except KeyboardInterrupt:
        print("\n👋 השרת נעצר")
    except Exception as e:
        print(f"❌ שגיאה: {e}")

if __name__ == "__main__":
    restart_server()
