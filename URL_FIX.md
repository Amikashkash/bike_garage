# 🔧 תיקון שגיאת NoReverseMatch ברשימת לקוחות

## 🐛 הבעיה:
```
NoReverseMatch: Reverse for 'customer_with_bike_form' not found
```

## 🔍 סיבת הבעיה:
בתבנית `customer_list.html` השתמשתי בשם URL שגוי:
```django
{% url 'customer_with_bike_form' %}  <!-- ❌ שם שגוי -->
```

אבל ב-`urls.py` השם האמיתי הוא:
```python
path('manager/customer-bike/new/', views.customer_with_bike_form, name='customer_with_bike_new'),
```

## ✅ הפתרון:
תיקנתי את השם ב-customer_list.html:

### לפני:
```django
{% url 'customer_with_bike_form' %}
```

### אחרי:
```django
{% url 'customer_with_bike_new' %}
```

## 📝 רשימת URLs נכונה:
בהתבסס על `urls.py`, השמות הנכונים הם:

| תכונה | שם URL | נתיב |
|--------|---------|------|
| טופס לקוח חדש | `customer_form` | `/customer/new/` |
| לקוח+אופניים חדש | `customer_with_bike_new` | `/manager/customer-bike/new/` |
| עריכת לקוח+אופניים | `customer_with_bike_edit` | `/manager/customer/<id>/bike/<id>/edit/` |
| הוספת אופניים ללקוח | `customer_bike_add` | `/manager/customer/<id>/bike/new/` |

## 🧪 איך לבדוק:

1. **הרץ את השרת:**
   ```bash
   python manage.py runserver
   ```

2. **בדוק את רשימת הלקוחות:**
   - התחבר כמנהל
   - לחץ על "רשימת לקוחות"
   - ✅ הדף אמור להטען ללא שגיאה

3. **בדוק את הכפתורים:**
   - ✅ "הוסף לקוח חדש" עובד
   - ✅ "לקוח + אופניים" עובד (חדש!)
   - ✅ כפתורי "ערוך" ו"הוסף אופניים" עובדים

## 📁 קבצים ששונו:
- `workshop/templates/workshop/customer_list.html` - תיקון שם URL

## 💡 למניעת בעיות דומות:
תמיד בדוק את `urls.py` לוודא את השם הנכון של URL patterns:

```bash
# חיפוש מהיר בקובץ URLs
grep "name=" workshop/urls.py
```

---

**🎯 התוצאה:** רשימת הלקוחות עובדת שוב וכל הכפתורים פונקציונליים!
