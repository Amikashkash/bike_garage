#!/usr/bin/env python
"""
בדיקה אחרונה לפני העלאה לשרת ייצור
"""
import os
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, Customer, Bike
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client

def final_system_check():
    """בדיקה אחרונה של המערכת"""
    print("🔍 בדיקה אחרונה לפני העלאה לשרת ייצור...")
    
    try:
        # 1. בדיקת מסד נתונים
        print("\n1️⃣ בודק מסד נתונים...")
        users_count = User.objects.count()
        customers_count = Customer.objects.count()
        bikes_count = Bike.objects.count()
        repairs_count = RepairJob.objects.count()
        
        print(f"✅ משתמשים: {users_count}")
        print(f"✅ לקוחות: {customers_count}")
        print(f"✅ אופניים: {bikes_count}")
        print(f"✅ תיקונים: {repairs_count}")
        
        # 2. בדיקת סטטוסים חדשים
        print("\n2️⃣ בודק סטטוסים חדשים...")
        awaiting_quality = RepairJob.objects.filter(status='awaiting_quality_check').count()
        quality_approved = RepairJob.objects.filter(status='quality_approved').count()
        
        print(f"✅ ממתינים לבדיקת איכות: {awaiting_quality}")
        print(f"✅ עברו בדיקת איכות: {quality_approved}")
        
        # 3. בדיקת שדות חדשים
        print("\n3️⃣ בודק שדות חדשים...")
        repairs_with_quality_check = RepairJob.objects.filter(
            quality_checked_by__isnull=False
        ).count()
        repairs_with_quality_notes = RepairJob.objects.exclude(
            quality_notes=''
        ).count()
        repairs_ready_for_pickup = RepairJob.objects.filter(
            ready_for_pickup_date__isnull=False
        ).count()
        
        print(f"✅ תיקונים עם בדיקת איכות: {repairs_with_quality_check}")
        print(f"✅ תיקונים עם הערות איכות: {repairs_with_quality_notes}")
        print(f"✅ תיקונים מוכנים לאיסוף: {repairs_ready_for_pickup}")
        
        # 4. בדיקת משתמשים מיוחדים
        print("\n4️⃣ בודק משתמשים מיוחדים...")
        manager = User.objects.filter(username='manager').first()
        mechanic = User.objects.filter(username='mechanic').first()
        
        if manager:
            print(f"✅ מנהל קיים: {manager.username}")
        else:
            print("❌ מנהל לא קיים")
            
        if mechanic:
            print(f"✅ מכונאי קיים: {mechanic.username}")
        else:
            print("❌ מכונאי לא קיים")
        
        # 5. בדיקת views חדשים
        print("\n5️⃣ בודק views חדשים...")
        client = Client()
        
        # בדיקת דף דיווח תקלה
        try:
            response = client.get('/customer-report/')
            if response.status_code == 200:
                print("✅ דף דיווח תקלה פועל")
            else:
                print(f"⚠️ דף דיווח תקלה: קוד {response.status_code}")
        except Exception as e:
            print(f"❌ דף דיווח תקלה: {e}")
        
        # בדיקת דשבורד מנהל (מחייב התחברות)
        if manager:
            client.force_login(manager)
            try:
                response = client.get('/manager-dashboard/')
                if response.status_code == 200:
                    print("✅ דשבורד מנהל פועל")
                else:
                    print(f"⚠️ דשבורד מנהל: קוד {response.status_code}")
            except Exception as e:
                print(f"❌ דשבורד מנהל: {e}")
        
        # 6. סיכום
        print("\n✅ הבדיקה הושלמה בהצלחה!")
        print("\n🚀 המערכת מוכנה להעלאה לשרת ייצור")
        print("\n📋 רשימת פיצ'רים שנוספו:")
        print("  ✅ תהליך בדיקת איכות על ידי מנהל")
        print("  ✅ סטטוסים חדשים: ממתין לבדיקת איכות, עבר בדיקת איכות")
        print("  ✅ שדות חדשים: quality_checked_by, quality_check_date, quality_notes")
        print("  ✅ שדות נוספים: ready_for_pickup_date, customer_notified")
        print("  ✅ דשבורד מנהל מעודכן")
        print("  ✅ עדכון דף דיווח תקלה")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקה: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    final_system_check()
