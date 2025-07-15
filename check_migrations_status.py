#!/usr/bin/env python
"""
בדיקה אם migrations רצו על השרת - בדיקת השדות החדשים
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection
from workshop.models import RepairJob

def check_migrations_status():
    """בדיקה אם המיגרציות החדשות רצו"""
    print("🔍 בודק סטטוס migrations בשרת...")
    
    try:
        # בדיקה אם השדות החדשים קיימים במסד הנתונים
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(workshop_repairjob);")
        columns = [row[1] for row in cursor.fetchall()]
        
        new_columns = [
            'quality_checked_by_id',
            'quality_check_date', 
            'quality_notes',
            'ready_for_pickup_date',
            'customer_notified'
        ]
        
        print("\n📊 בדיקת עמודות חדשות:")
        all_exist = True
        for col in new_columns:
            exists = col in columns
            status = "✅" if exists else "❌"
            print(f"   {status} {col}: {'קיים' if exists else 'לא קיים'}")
            if not exists:
                all_exist = False
        
        # בדיקה אם max_length של status השתנה
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='workshop_repairjob';")
        table_schema = cursor.fetchone()[0]
        
        print(f"\n📝 סכמת טבלה:")
        if 'status VARCHAR(30)' in table_schema:
            print("   ✅ שדה status עודכן לגודל 30")
        elif 'status VARCHAR(20)' in table_schema:
            print("   ⚠️ שדה status עדיין בגודל 20")
        else:
            print("   ❓ לא ניתן לזהות גודל שדה status")
        
        # בדיקה אם הסטטוסים החדשים עובדים
        print(f"\n🧪 בדיקת סטטוסים חדשים:")
        try:
            awaiting_count = RepairJob.objects.filter(status='awaiting_quality_check').count()
            approved_count = RepairJob.objects.filter(status='quality_approved').count()
            
            print(f"   🔍 ממתינים לבדיקת איכות: {awaiting_count}")
            print(f"   ✅ מוכנים לאיסוף: {approved_count}")
            print("   ✅ הסטטוסים החדשים עובדים!")
        except Exception as e:
            print(f"   ❌ שגיאה בסטטוסים חדשים: {e}")
            all_exist = False
        
        # סיכום
        print(f"\n{'='*50}")
        if all_exist:
            print("🎉 כל המיגרציות רצו בהצלחה!")
            print("✅ השרת מוכן לתכונות בדיקת האיכות החדשות")
        else:
            print("⚠️ יש בעיות עם המיגרציות")
            print("💡 אולי צריך לחכות עוד קצת או לכפות deploy ידני ב-Render")
            
        return all_exist
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקת מיגרציות: {e}")
        return False

def check_render_deployment():
    """בדיקה אם השרת זמין ומעודכן"""
    print(f"\n🌐 בדיקת זמינות שרת...")
    import requests
    import time
    
    try:
        # נסיון להגיע לדשבורד מנהל
        response = requests.get('https://bikegarage-4yjs.onrender.com/manager-dashboard/', timeout=10)
        
        if response.status_code == 200:
            print("   ✅ שרת זמין ומגיב")
            
            # בדיקה אם יש את הקטגוריות החדשות
            if 'ממתינים לבדיקת איכות' in response.text:
                print("   ✅ קטגוריות בדיקת איכות זמינות!")
                return True
            else:
                print("   ⚠️ עדיין לא רואה את הקטגוריות החדשות")
                return False
        else:
            print(f"   ⚠️ שרת מחזיר קוד: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ שגיאה בגישה לשרת: {e}")
        return False

if __name__ == "__main__":
    migrations_ok = check_migrations_status()
    server_ok = check_render_deployment()
    
    if migrations_ok and server_ok:
        print("\n🚀 הכל מוכן! אפשר לבדוק את התכונות החדשות")
    elif migrations_ok:
        print("\n⏳ מיגרציות אוקיי, אבל השרת עדיין מתעדכן...")
    else:
        print("\n🔄 עדיין מחכה למיגרציות...")
        
    print("\n💡 אם יש בעיות, נסה:")
    print("   1. לחכות עוד 2-3 דקות")
    print("   2. להכנס לדשבורד Render ולכפות deploy חדש")
    print("   3. לבדוק את ה-logs ב-Render")
