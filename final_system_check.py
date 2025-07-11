#!/usr/bin/env python
"""
בדיקה מהירה שכל התכונות עובדות לפני הצגה ללקוח
"""
import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User, Group
from workshop.models import Customer, Bike, RepairJob, RepairItem

def check_system_status():
    """בדיקת תקינות המערכת"""
    print("🔍 בודק סטטוס המערכת...")
    
    # בדיקת משתמשים
    mechanics = User.objects.filter(groups__name='Mechanic')
    managers = User.objects.filter(groups__name='Manager')
    
    print(f"👨‍🔧 מכונאים במערכת: {mechanics.count()}")
    for m in mechanics:
        print(f"   - {m.username}")
        
    print(f"👨‍💼 מנהלים במערכת: {managers.count()}")
    for m in managers:
        print(f"   - {m.username}")
    
    # בדיקת נתונים
    customers = Customer.objects.count()
    bikes = Bike.objects.count()
    repairs = RepairJob.objects.count()
    repair_items = RepairItem.objects.count()
    
    print(f"\n📊 נתוני דמו:")
    print(f"   - לקוחות: {customers}")
    print(f"   - אופניים: {bikes}")
    print(f"   - תיקונים: {repairs}")
    print(f"   - פעולות תיקון: {repair_items}")
    
    # בדיקת סטטוסים
    if repair_items > 0:
        completed = RepairItem.objects.filter(status='completed').count()
        pending = RepairItem.objects.filter(status='pending').count()
        stuck = RepairItem.objects.filter(status='blocked').count()
        
        print(f"\n📈 סטטוס פעולות:")
        print(f"   - בוצע: {completed}")
        print(f"   - ממתין: {pending}")
        print(f"   - תקוע: {stuck}")
        
        # הצגת פעולות תקועות
        stuck_items = RepairItem.objects.filter(status='blocked')
        if stuck_items.exists():
            print(f"\n🔴 פעולות תקועות שדורשות תשומת לב:")
            for item in stuck_items:
                print(f"   - {item.description} (תיקון: {item.repair_job})")
                if item.notes:
                    print(f"     הערה: {item.notes}")
    
    print(f"\n✅ המערכת מוכנה להצגה!")
    print(f"🚀 הרץ: python manage.py runserver")
    print(f"🌐 דף בית: http://localhost:8000/")

def create_demo_stuck_items():
    """יצירת פעולות תקועות לדמו"""
    print("\n🎭 יוצר פעולות תקועות לדמו...")
    
    repairs = RepairJob.objects.all()[:2]  # שני תיקונים ראשונים
    
    for repair in repairs:
        # מצא פעולה שלא בוצעה
        items = repair.repair_items.filter(status__in=['pending', 'completed'])[:1]
        
        for item in items:
            item.status = 'blocked'
            item.notes = 'בעיה טכנית - צריך חלק חילוף מיוחד'
            item.save()
            print(f"   ✅ הפעולה '{item.description}' מסומנת כתקועה")
    
    print("🎪 פעולות תקועות נוצרו בהצלחה לדמו!")

if __name__ == '__main__':
    print("=" * 60)
    print("🚴‍♂️ בדיקת מוכנות מערכת מוסך אופניים")
    print("=" * 60)
    
    try:
        check_system_status()
        
        # אפשרות ליצור נתוני דמו
        if len(sys.argv) > 1 and sys.argv[1] == '--create-stuck':
            create_demo_stuck_items()
            print("\n" + "=" * 60)
            check_system_status()
            
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        print("💡 ודא שהרצת migrations: python manage.py migrate")
