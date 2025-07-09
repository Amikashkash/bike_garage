"""
סקריפט להרצת השרת ובדיקת הטופס
"""
import subprocess
import webbrowser
import time
import sys
import os

def run_server():
    """הרצת השרת של Django"""
    try:
        print("🚀 מתחיל השרת Django...")
        # שינוי לתיקיית הפרויקט
        os.chdir(r'c:\bikegarage')
        
        # הפעלת השרת
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        return process
        
    except Exception as e:
        print(f"❌ שגיאה בהרצת השרת: {e}")
        return None

def main():
    print("🏠 מערכת ניהול מוסך אופניים")
    print("=" * 40)
    
    # הרצת השרת
    server_process = run_server()
    if not server_process:
        print("❌ נכשל בהפעלת השרת")
        return
    
    # המתנה לטעינת השרת
    print("⏳ ממתין לטעינת השרת...")
    time.sleep(4)
    
    print("\n📋 מידע התחברות:")
    print("   🌐 כתובת: http://localhost:8000/")
    print("   👤 משתמש לקוח: customer_test")
    print("   🔑 סיסמה: test123456")
    print("   🎨 טופס אישור מעודכן: http://localhost:8000/repair/5/approve/")
    print("\n⭐ חדש! עיצוב מעודכן:")
    print("   🎯 בחירה סלקטיבית של פעולות תיקון")
    print("   � חישוב מחיר דינמי בזמן אמת")
    print("   🎨 ממשק משתמש מודרני ויפה")
    print("   📱 תמיכה מלאה במכשירים ניידים")
    print("\n�📌 מידע נוסף:")
    print("   📧 ניתן לבדוק גם משתמשי מנהל/מכונאי")
    print("   🔧 ניתן ליצור משתמשים חדשים דרך /register/")
    print("   📖 קרא DESIGN_SUMMARY.md לפרטים על העיצוב החדש")
    
    # פתיחת הדפדפן
    print("\n🌐 פותח דפדפן...")
    try:
        webbrowser.open('http://localhost:8000/')
    except Exception as e:
        print(f"⚠️ לא ניתן לפתוח דפדפן אוטומטית: {e}")
    
    print("\n✅ השרת רץ בהצלחה!")
    print("🛑 לחץ Ctrl+C לעצירה")
    
    try:
        # המתנה עד לעצירה ידנית
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 עוצר את השרת...")
        server_process.terminate()
        server_process.wait()
        print("✅ השרת נעצר")

if __name__ == "__main__":
    main()
