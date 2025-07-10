#!/usr/bin/env python
"""
סקריפט לכניסה אוטומטית וצילום מסך של הממשק
"""

import webbrowser
import time
import os

def open_mechanic_interface():
    print("=== פתיחת ממשק טכנאי ===")
    
    url = "http://localhost:8000/mechanic/task/2/"
    
    print(f"🌐 פותח: {url}")
    print(f"👤 משתמש: mechanic_test")
    print(f"🔑 סיסמה: mechanic123")
    
    # פתיחה בדפדפן
    webbrowser.open(url)
    
    print("\n📋 מה לבדוק:")
    print("1. התחבר כמשתמש mechanic_test")
    print("2. בדוק שבכותרת הטבלה יש: 'הערות / מה מונע מביצוע'")
    print("3. סמן צ'קבוקס 'חסום' ובדוק שמופיע: 'מה מונע ממך להתקדם?'")
    print("4. סמן צ'קבוקס 'בוצע' ובדוק שמופיע: 'הערות נוספות (אופציונלי)'")
    
    print("\n🔧 אם עדיין רואה טקסט ישן:")
    print("- לחץ Ctrl+F5 (Hard Refresh)")
    print("- או פתח חלון פרטי/incognito")
    print("- או נקה cache של הדפדפן")
    
    print("\n💡 אם זה לא עוזר, ייתכן שיש בעיה בשרת או בקובץ")

if __name__ == "__main__":
    open_mechanic_interface()
