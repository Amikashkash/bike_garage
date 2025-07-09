#!/usr/bin/env python3
"""
🔧 בדיקה מהירה לתיקון תבנית customer_list.html
"""

import os
import sys
import django

# הוספת נתיב הפרויקט
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

try:
    django.setup()
    
    from django.template.loader import get_template
    from django.template import Context
    from workshop.models import Customer
    
    print("🧪 בודק תבנית customer_list.html...")
    
    # בדיקת טעינת התבנית
    try:
        template = get_template('workshop/customer_list.html')
        print("✅ התבנית נטענת ללא שגיאה")
    except Exception as e:
        print(f"❌ שגיאה בטעינת התבנית: {e}")
        sys.exit(1)
    
    # הכנת נתונים לבדיקה
    customers_with_user = Customer.objects.filter(user__isnull=False)
    customers_without_user = Customer.objects.filter(user__isnull=True)
    
    context = {
        'customers_with_user': customers_with_user,
        'customers_without_user': customers_without_user,
    }
    
    # בדיקת רינדור התבנית
    try:
        rendered = template.render(context)
        print("✅ התבנית מתרנדרת ללא שגיאה")
        print(f"📏 אורך התוכן שנוצר: {len(rendered)} תווים")
        
        # בדיקה שהתוכן מכיל את מה שאנחנו מצפים
        if 'רשימת לקוחות' in rendered:
            print("✅ כותרת הדף קיימת")
        if 'לקוחות רשומים במערכת' in rendered:
            print("✅ קטגוריית הלקוחות הרשומים קיימת")
        if 'פרטי קשר בלבד' in rendered:
            print("✅ קטגוריית פרטי הקשר קיימת")
            
    except Exception as e:
        print(f"❌ שגיאה ברינדור התבנית: {e}")
        sys.exit(1)
    
    print("🎉 כל הבדיקות עברו בהצלחה!")
    print("💡 עכשיו אפשר לנסות לגשת לרשימת הלקוחות בדפדפן")
    
except Exception as e:
    print(f"❌ שגיאה כללית: {e}")
    sys.exit(1)
