🚵‍♂️ ENDURO BIKE GARAGE - הוראות התחברות למנהל

כדי לגשת לדשבורד המנהל, יש צורך ליצור משתמש מנהל.

🔧 שלבים:

1. פתח את הטרמינל בתיקיית הפרויקט
2. הפעל: python manage.py shell
3. הכנס את הקוד הבא:

```python
from django.contrib.auth.models import User
from workshop.models import UserProfile

# יצירת משתמש מנהל
user = User.objects.create_superuser(
    username='manager',
    email='manager@endurobikegarage.com', 
    password='manager123'
)

# יצירת פרופיל מנהל
UserProfile.objects.create(user=user, role='manager')

print("✅ משתמש מנהל נוצר בהצלחה!")
```

4. לחץ Ctrl+D ליציאה
5. גש לכתובת: http://127.0.0.1:8000/login/
6. התחבר עם:
   - שם משתמש: manager
   - סיסמה: manager123
7. גש לדשבורד: http://127.0.0.1:8000/manager/dashboard/

🎯 המערכת תעבוד עם העיצוב האקסטרימי החדש!

📱 אם אין נתונים, המערכת תציג מסך ריק יפה.
🚀 ניתן להוסיף נתוני דמו דרך ממשק הניהול.
