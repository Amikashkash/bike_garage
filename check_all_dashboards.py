#!/usr/bin/env python
"""
בדיקה מהירה של כל הדשבורדים
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from workshop.models import UserProfile, RepairJob

def test_all_dashboards():
    """בדיקת כל הדשבורדים"""
    print("🔍 בודק את כל הדשבורדים...")
    
    client = Client()
    
    # 1. בדיקת דשבורד מנהל
    print("\n1️⃣ בדיקת דשבורד מנהל...")
    try:
        manager = User.objects.filter(userprofile__role='manager').first()
        if manager:
            client.force_login(manager)
            response = client.get('/manager-dashboard/')
            print(f"   ✅ דשבורד מנהל: {response.status_code}")
            if response.status_code != 200:
                print(f"   ❌ שגיאה: {response.content.decode()[:200]}")
        else:
            print("   ⚠️ לא נמצא מנהל במערכת")
    except Exception as e:
        print(f"   ❌ שגיאה בדשבורד מנהל: {e}")
    
    # 2. בדיקת דשבורד מכונאי
    print("\n2️⃣ בדיקת דשבורד מכונאי...")
    try:
        mechanic = User.objects.filter(userprofile__role='mechanic').first()
        if mechanic:
            client.force_login(mechanic)
            response = client.get('/mechanic-dashboard/')
            print(f"   ✅ דשבורד מכונאי: {response.status_code}")
            if response.status_code != 200:
                print(f"   ❌ שגיאה: {response.content.decode()[:200]}")
        else:
            print("   ⚠️ לא נמצא מכונאי במערכת")
    except Exception as e:
        print(f"   ❌ שגיאה בדשבורד מכונאי: {e}")
    
    # 3. בדיקת דף דיווח לקוח
    print("\n3️⃣ בדיקת דף דיווח לקוח...")
    try:
        customer = User.objects.filter(userprofile__role='customer').first()
        if customer:
            client.force_login(customer)
            response = client.get('/customer-report/')
            print(f"   ✅ דף דיווח לקוח: {response.status_code}")
            if response.status_code != 200:
                print(f"   ❌ שגיאה: {response.content.decode()[:200]}")
        else:
            print("   ⚠️ לא נמצא לקוח במערכת")
    except Exception as e:
        print(f"   ❌ שגיאה בדף דיווח לקוח: {e}")
    
    # 4. בדיקת דף הרשמה
    print("\n4️⃣ בדיקת דף הרשמה...")
    try:
        client.logout()
        response = client.get('/register/')
        print(f"   ✅ דף הרשמה: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ שגיאה: {response.content.decode()[:200]}")
    except Exception as e:
        print(f"   ❌ שגיאה בדף הרשמה: {e}")
    
    # 5. בדיקת דף בית
    print("\n5️⃣ בדיקת דף בית...")
    try:
        response = client.get('/')
        print(f"   ✅ דף בית: {response.status_code}")
        if response.status_code != 200:
            print(f"   ❌ שגיאה: {response.content.decode()[:200]}")
    except Exception as e:
        print(f"   ❌ שגיאה בדף בית: {e}")
    
    # סטטיסטיקות
    print("\n📊 סטטיסטיקות מערכת:")
    print(f"   👥 משתמשים: {User.objects.count()}")
    print(f"   🔧 תיקונים: {RepairJob.objects.count()}")
    print(f"   👨‍💼 מנהלים: {User.objects.filter(userprofile__role='manager').count()}")
    print(f"   🔧 מכונאים: {User.objects.filter(userprofile__role='mechanic').count()}")
    print(f"   👤 לקוחות: {User.objects.filter(userprofile__role='customer').count()}")
    
    print("\n✅ בדיקה הושלמה!")

if __name__ == "__main__":
    test_all_dashboards()
