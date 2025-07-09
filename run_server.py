"""
מערכת ניהול מוסך אופניים - הפעלת השרת
"""
import subprocess
import webbrowser
import time
import sys
import os

def main():
    print("🚴‍♂️ מערכת ניהול מוסך אופניים")
    print("=" * 50)
    
    # וידוא שאנחנו בתיקיה הנכונה
    if not os.path.exists('manage.py'):
        print("❌ שגיאה: הפעל את הסקריפט מתיקיית הפרויקט")
        return
    
    print("🚀 מפעיל שרת Django...")
    print("⏳ השרת יפתח בדפדפן תוך מספר שניות...")
    
    # הרצת השרת בצורה שמציגה לוגים
    try:
        # פתיחת דפדפן אחרי 3 שניות
        import threading
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:8000/')
            except:
                pass
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        print("\n📋 מידע חשוב:")
        print("   🌐 כתובת: http://localhost:8000/")
        print("   👤 משתמש לקוח: customer_test")
        print("   🔑 סיסמה: test123456")
        print("   🎯 טופס אישור: http://localhost:8000/repair/5/approve/")
        print("\n⭐ התכונה החדשה:")
        print("   ✅ בחירה סלקטיבית של פעולות תיקון")
        print("   💰 חישוב מחיר דינמי")
        print("   🎨 עיצוב מודרני ויפה")
        print("\n🛑 לחץ Ctrl+C לעצירת השרת")
        print("-" * 50)
        
        # הפעלת השרת (יציג לוגים)
        subprocess.run([sys.executable, 'manage.py', 'runserver'], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 השרת נעצר")
    except subprocess.CalledProcessError as e:
        print(f"❌ שגיאה בהרצת השרת: {e}")
    except Exception as e:
        print(f"❌ שגיאה: {e}")

if __name__ == "__main__":
    main()
