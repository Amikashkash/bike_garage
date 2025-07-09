#!/usr/bin/env python3
"""
🔧 סקריפט בדיקה מהירה לנאבבר מובייל
"""

import os
import subprocess
import sys
import webbrowser
import time

def main():
    print("🚀 בדיקה מהירה לנאבבר החדש")
    print("=" * 50)
    
    # בדיקה שאנחנו בתיקיה הנכונה
    if not os.path.exists('manage.py'):
        print("❌ אנא הרץ את הסקריפט מתיקיית הפרויקט")
        return
    
    print("📋 רשימת בדיקות:")
    print("1. הרצת השרת")
    print("2. פתיחת הדפדפן")
    print("3. הנחיות לבדיקה במובייל")
    print()
    
    # הרצת השרת
    print("🚀 מתחיל שרת...")
    try:
        # נסה לפתוח את הדפדפן
        time.sleep(2)
        webbrowser.open('http://localhost:8000')
        print("🌐 הדפדפן נפתח. בדוק:")
        print("   ✓ לחץ F12 לפתיחת DevTools")
        print("   ✓ לחץ Ctrl+Shift+M לעמוד למצב מובייל") 
        print("   ✓ בחר iPhone או Android בסימולטור")
        print("   ✓ בדוק שיש hamburger menu (☰)")
        print("   ✓ לחץ על hamburger ובדוק שהתפריט נפתח")
        print()
        
        print("📱 לבדיקה במובייל אמיתי:")
        print("   1. הרץ את start_mobile_server.bat")
        print("   2. השתמש בכתובת שמוצגת")
        print("   3. בדוק שהתפריט עובד במובייל")
        print()
        
        print("⚠️  לעצירת השרת לחץ Ctrl+C")
        
        # הרצת השרת
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
        
    except KeyboardInterrupt:
        print("\n✅ השרת נעצר")
    except Exception as e:
        print(f"❌ שגיאה: {e}")

if __name__ == "__main__":
    main()
