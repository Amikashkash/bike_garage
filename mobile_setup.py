#!/usr/bin/env python3
"""
מציאת כתובת IP מקומית לגישה מובייל
"""

import socket
import subprocess
import platform

def get_local_ip():
    """מקבל את כתובת ה-IP המקומית"""
    try:
        # יצירת חיבור dummy כדי למצוא את ה-IP המקומי
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return None

def show_mobile_instructions():
    """הצגת הוראות לגישה מובייל"""
    
    print("📱 הגדרת גישה למערכת מסמרטפון")
    print("=" * 50)
    print()
    
    local_ip = get_local_ip()
    
    if local_ip:
        print(f"🌐 כתובת IP של המחשב: {local_ip}")
        print(f"📱 גש מהמובייל לכתובת: http://{local_ip}:8000")
        print()
        print("📋 שלבים:")
        print("1. וודא שהמחשב והמובייל חיברים לאותה רשת WiFi")
        print("2. הרץ את השרת: python manage.py runserver 0.0.0.0:8000")
        print(f"3. פתח דפדפן במובייל ועבור ל: http://{local_ip}:8000")
        print()
        print("💡 טיפים נוספים:")
        print("- אם לא עובד, בדוק firewall במחשב")
        print("- במכשירי Android: Chrome / Firefox")
        print("- במכשירי iPhone: Safari / Chrome")
        print("- שמור את הכתובת כסימנייה למהירות")
    else:
        print("❌ לא הצלחתי למצוא כתובת IP מקומית")
        print("💡 בדוק שאתה מחובר לרשת WiFi")
        print()
        print("🔧 ניסיון ידני:")
        if platform.system() == "Windows":
            print("הרץ: ipconfig")
        else:
            print("הרץ: ifconfig או ip addr")
        print("חפש כתובת שמתחילה ב-192.168. או 10.")
    
    print()
    print("🎨 העיצוב מותאם לנייד עם Bootstrap responsive!")

if __name__ == "__main__":
    show_mobile_instructions()
