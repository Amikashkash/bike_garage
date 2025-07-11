# 🚀 מדריך עבודה עם Localhost ו-Production

## העקרונות הבסיסיים

### 1. פיתוח מקומי (Localhost)
- **תמיד** פתח ובדוק שינויים מקומית לפני push
- השתמש בשרת הפיתוח המקומי לבדיקות
- בדוק את כל הפיצ'רים לפני commit

### 2. Staging/Testing
- בדוק שהכל עובד לפני push
- הרץ את כל הסקריפטים לבדיקת תקינות
- ודא שאין שגיאות

### 3. Production Push
- דחוף רק קוד מוכן ובדוק
- השתמש בcommit messages ברורים
- עקוב אחרי ה-deployment בRender

---

## הגדרת Workflow מומלץ

### שלב 1: הגדרות Environment
```bash
# בקובץ .env (לא נדחף לgit)
DEBUG=True
SECRET_KEY=your-local-secret-key
DATABASE_URL=sqlite:///db.sqlite3

# ב-production (Render Environment Variables):
DEBUG=False
SECRET_KEY=production-secret
DATABASE_URL=postgresql://...
```

### שלב 2: פקודות עבודה יומיות

#### התחלת עבודה:
```bash
cd c:\bikegarage
# הפעלת environment
venv\Scripts\activate
# עדכון מהgit
git pull origin main
# הרצת שרת מקומי
python manage.py runserver
```

#### בדיקת שינויים:
```bash
# בדיקת תקינות המערכת
python check_production_errors.py

# בדיקת migrations
python manage.py makemigrations
python manage.py migrate

# בדיקת static files
python manage.py collectstatic

# בדיקת כל הפיצ'רים בדפדפן
# http://127.0.0.1:8000/
```

#### לפני Push:
```bash
# בדיקה סופית
python check_production_errors.py

# וידוא שהכל עובד
python manage.py runserver
# בדוק בדפדפן: http://127.0.0.1:8000/

# רק אם הכל בסדר:
git add .
git commit -m "תיאור ברור של השינוי"
git push origin main
```

---

## סקריפטים לעבודה נוחה

### סקריפט התחלת עבודה - start_work.py
```python
import subprocess
import os

def start_development():
    print("🚀 התחלת סביבת פיתוח...")
    
    # activate virtual environment
    os.system("venv\\Scripts\\activate")
    
    # עדכון מgit
    print("📥 עדכון מ-git...")
    subprocess.run(["git", "pull", "origin", "main"])
    
    # בדיקת migrations
    print("🔍 בדיקת migrations...")
    subprocess.run(["python", "manage.py", "migrate"])
    
    # הרצת בדיקות תקינות
    print("✅ בדיקת תקינות...")
    subprocess.run(["python", "check_production_errors.py"])
    
    print("🎉 מוכן לעבודה!")
    print("הרץ: python manage.py runserver")

if __name__ == "__main__":
    start_development()
```

### סקריפט בדיקה לפני Push - pre_push_check.py
```python
import subprocess
import sys

def pre_push_check():
    print("🔍 בדיקה לפני Push...")
    
    checks = [
        ("בדיקת תקינות", ["python", "check_production_errors.py"]),
        ("בדיקת migrations", ["python", "manage.py", "makemigrations", "--dry-run"]),
        ("בדיקת static files", ["python", "manage.py", "collectstatic", "--dry-run"]),
    ]
    
    all_passed = True
    
    for check_name, command in checks:
        print(f"\n📋 {check_name}...")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {check_name} - OK")
            else:
                print(f"❌ {check_name} - FAILED")
                print(result.stderr)
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} - ERROR: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 כל הבדיקות עברו - מוכן לPush!")
        return True
    else:
        print("\n⚠️ יש בעיות - אל תעשה Push עדיין!")
        return False

if __name__ == "__main__":
    if pre_push_check():
        print("\nלdeploy הרץ:")
        print("git add .")
        print('git commit -m "תיאור השינוי"')
        print("git push origin main")
    sys.exit(0 if pre_push_check() else 1)
```

---

## טיפים חשובים

### 🔧 פיתוח בטוח
1. **עבוד תמיד עם branch** (אופציונלי מתקדם):
   ```bash
   git checkout -b feature-new-feature
   # עבוד על השינוי
   git commit -m "שינוי חדש"
   git checkout main
   git merge feature-new-feature
   git push origin main
   ```

2. **השתמש ב-.env לhemevelopment**:
   ```bash
   # צור קובץ .env בתיקיית הפרויקט
   DEBUG=True
   SECRET_KEY=dev-secret-key-123
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

3. **בדוק logs לפני push**:
   ```bash
   # תמיד בדוק בconsole שאין שגיאות
   python manage.py runserver
   # לך לדפדפן ובדוק: http://127.0.0.1:8000/
   ```

### 🚀 Deployment בטוח
1. **עקוב אחרי deployment בRender**
2. **בדוק logs אחרי push**
3. **אם יש שגיאה - תקן מיד**

### 🔍 בדיקות חובה לפני Push
- [ ] השרת המקומי רץ ללא שגיאות
- [ ] כל הדפים נטענים
- [ ] הרשמה/התחברות עובדים
- [ ] אין שגיאות בconsole
- [ ] `check_production_errors.py` עובר בהצלחה

---

## קבצים להוסיף ל-.gitignore
```
# הוסף לקובץ .gitignore
.env
*.log
__pycache__/
.vscode/
.idea/
*.pyc
```

זה יבטיח שקבצי פיתוח מקומיים לא יידחפו לproduction.
