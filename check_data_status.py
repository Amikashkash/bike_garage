#!/usr/bin/env python
"""
בדיקת מצב הנתונים בפועל במערכת
"""
import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from workshop.models import RepairJob, RepairItem, Customer, Bike
from django.contrib.auth.models import User
from workshop.models import UserProfile

def check_real_data():
    print("🔍 בדיקת נתונים אמיתיים במערכת...")
    
    # בדיקת כל התיקונים
    repairs = RepairJob.objects.all()
    print(f"📋 סה\"ג תיקונים במערכת: {repairs.count()}")
    
    for repair in repairs:
        print(f"\n🔧 תיקון #{repair.id}:")
        print(f"   לקוח: {repair.bike.customer}")
        print(f"   סטטוס: {repair.status}")
        print(f"   אופניים: {repair.bike}")
        print(f"   פריטי תיקון: {repair.repair_items.count()}")
        
        if repair.repair_items.exists():
            for item in repair.repair_items.all():
                status = "✅ מאושר" if item.is_approved_by_customer else "⏳ ממתין"
                print(f"     - {item.description}: ₪{item.price} ({status})")
        
        # בדיקה אם התיקון זמין לאישור לקוח
        if repair.status in ['diagnosed', 'partially_approved']:
            print(f"   🎯 זמין לאישור לקוח: http://localhost:8000/repair/{repair.id}/approve/")
            
            # בדיקה אם יש משתמש מחובר ללקוח
            if hasattr(repair.bike.customer, 'user') and repair.bike.customer.user:
                print(f"   👤 משתמש מחובר: {repair.bike.customer.user.username}")
            else:
                print(f"   ⚠️ אין משתמש מחובר ללקוח")

def create_technician(username, first_name="טכנאי", last_name="חדש"):
    """יצירת טכנאי חדש במערכת"""
    
    # בדיקה אם הטכנאי כבר קיים
    if User.objects.filter(username=username).exists():
        print(f"❌ הטכנאי '{username}' כבר קיים!")
        user = User.objects.get(username=username)
        
        # בדיקה אם יש לו פרופיל
        try:
            profile = user.userprofile
            print(f"📋 פרטי הטכנאי: {user.first_name} {user.last_name}, תפקיד: {profile.role}")
            if profile.role != 'mechanic':
                profile.role = 'mechanic'
                profile.save()
                print(f"✅ תוקן תפקיד ל-mechanic")
            return user
        except UserProfile.DoesNotExist:
            # יצירת פרופיל אם לא קיים
            profile = UserProfile.objects.create(
                user=user,
                role='mechanic'
            )
            print(f"✅ נוצר פרופיל טכנאי חדש עבור: {user.username}")
            return user
    
    try:
        # יצירת משתמש חדש
        user = User.objects.create_user(
            username=username,
            email=f'{username}@bikegarage.test',
            password='test123',
            first_name=first_name,
            last_name=last_name
        )
        
        # יצירת פרופיל טכנאי
        profile = UserProfile.objects.create(
            user=user,
            role='mechanic'
        )
        
        print(f"✅ נוצר טכנאי חדש: {user.username}")
        print(f"📋 שם מלא: {user.first_name} {user.last_name}")
        print(f"🔧 תפקיד: {profile.role}")
        print(f"🔑 סיסמה: test123")
        
        return user
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת טכנאי: {e}")
        return None

def interactive_menu():
    """תפריט אינטראקטיבי לניהול המערכת"""
    
    while True:
        print("\n" + "="*50)
        print("🔧 מערכת ניהול המוסך - תפריט ראשי")
        print("="*50)
        print("1. בדיקת מצב נתונים")
        print("2. יצירת טכנאי חדש")
        print("3. רשימת כל הטכנאים")
        print("4. יציאה")
        print("-"*50)
        
        choice = input("בחר אפשרות (1-4): ").strip()
        
        if choice == "1":
            check_real_data()
        elif choice == "2":
            username = input("הכנס שם משתמש לטכנאי: ").strip()
            if username:
                first_name = input("שם פרטי (אופציונלי): ").strip() or "טכנאי"
                last_name = input("שם משפחה (אופציונלי): ").strip() or "חדש"
                create_technician(username, first_name, last_name)
            else:
                print("❌ חובה להכניס שם משתמש!")
        elif choice == "3":
            list_technicians()
        elif choice == "4":
            print("👋 להתראות!")
            break
        else:
            print("❌ בחירה לא חוקית!")

def list_technicians():
    """הצגת רשימת כל הטכנאים"""
    print("\n🔧 רשימת טכנאים במערכת:")
    print("-"*40)
    
    mechanics = UserProfile.objects.filter(role='mechanic')
    
    if not mechanics.exists():
        print("❌ אין טכנאים במערכת")
        return
    
    for i, profile in enumerate(mechanics, 1):
        user = profile.user
        print(f"{i}. {user.username} - {user.first_name} {user.last_name}")
        print(f"   📧 {user.email}")
        
        # בדיקת תיקונים מוקצים
        assigned_repairs = RepairJob.objects.filter(assigned_mechanic=user)
        print(f"   🔧 תיקונים מוקצים: {assigned_repairs.count()}")

if __name__ == "__main__":
    import sys
    
    # בדיקה אם הועברו ארגומנטים
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create" and len(sys.argv) > 2:
            # יצירת טכנאי מהשורת פקודה
            username = sys.argv[2]
            first_name = sys.argv[3] if len(sys.argv) > 3 else "טכנאי"
            last_name = sys.argv[4] if len(sys.argv) > 4 else "חדש"
            create_technician(username, first_name, last_name)
        elif command == "list":
            list_technicians()
        elif command == "check":
            check_real_data()
        else:
            print("❌ פקודה לא מוכרת!")
            print("שימוש:")
            print("  python check_data_status.py create <username> [first_name] [last_name]")
            print("  python check_data_status.py list")
            print("  python check_data_status.py check")
    else:
        # תפריט אינטראקטיבי
        interactive_menu()
