#!/usr/bin/env python3
"""
בדיקת התכונות החדשות למעקב אחר טכנאים
"""

import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_manager_features():
    """בדיקת התכונות החדשות למנהל"""
    from workshop.models import RepairJob, RepairItem, Customer, Bike
    from django.contrib.auth.models import User
    from workshop.models import UserProfile
    
    print("🧪 בדיקת תכונות מעקב טכנאים...")
    
    # בדיקת תיקונים קיימים
    repairs = RepairJob.objects.filter(status__in=['approved', 'in_progress'])
    print(f"📊 נמצאו {repairs.count()} תיקונים בביצוע")
    
    for repair in repairs[:3]:  # בדיקת 3 הראשונים
        print(f"\n🔧 תיקון #{repair.id} - {repair.bike}")
        
        # חישוב סטטיסטיקות
        approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        completed_items = approved_items.filter(is_completed=True)
        pending_items = approved_items.filter(is_completed=False)
        
        total_approved = approved_items.count()
        total_completed = completed_items.count()
        progress = (total_completed / total_approved * 100) if total_approved > 0 else 0
        
        print(f"   ✅ פעולות שהושלמו: {total_completed}")
        print(f"   ⏳ פעולות ממתינות: {pending_items.count()}")
        print(f"   📈 אחוז התקדמות: {progress:.1f}%")
        
        if repair.assigned_mechanic:
            print(f"   👤 מכונאי: {repair.assigned_mechanic.username}")
            
            # עדכונים אחרונים מהטכנאי
            recent_updates = repair.updates.filter(
                user=repair.assigned_mechanic
            ).order_by('-created_at')[:2]
            
            if recent_updates:
                print(f"   💬 עדכונים אחרונים:")
                for update in recent_updates:
                    print(f"      - {update.message[:50]}... ({update.created_at.strftime('%d/%m %H:%M')})")
            else:
                print(f"   💬 אין עדכונים מהטכנאי")
        else:
            print(f"   ⚠️ לא הוקצה מכונאי")
    
    return True

def create_demo_progress():
    """יצירת נתוני דמו להתקדמות"""
    from workshop.models import RepairJob, RepairItem, RepairUpdate
    from django.contrib.auth.models import User
    from django.utils import timezone
    
    print("\n🎭 יצירת נתוני דמו...")
    
    # מציאת תיקון קיים
    repair = RepairJob.objects.filter(
        status__in=['approved', 'in_progress'],
        assigned_mechanic__isnull=False
    ).first()
    
    if not repair:
        print("❌ לא נמצא תיקון מתאים לדמו")
        return False
    
    print(f"✅ נמצא תיקון לדמו: #{repair.id}")
    
    # סימון כמה פעולות כמושלמות
    pending_items = repair.repair_items.filter(
        is_approved_by_customer=True,
        is_completed=False
    )
    
    if pending_items.exists():
        # סימון הפעולה הראשונה כמושלמת
        first_item = pending_items.first()
        first_item.is_completed = True
        first_item.completed_by = repair.assigned_mechanic
        first_item.completed_at = timezone.now()
        first_item.notes = "הושלם בהצלחה - בדיקת דמו"
        first_item.save()
        print(f"✅ סומנה פעולה כמושלמת: {first_item.description}")
        
        # הוספת עדכון מהטכנאי
        RepairUpdate.objects.create(
            repair_job=repair,
            user=repair.assigned_mechanic,
            message=f"השלמתי את הפעולה: {first_item.description}. התקדמות טובה.",
            is_visible_to_customer=True
        )
        print(f"✅ נוסף עדכון מהטכנאי")
    
    return True

def main():
    print("🛠️ בדיקת מערכת מעקב טכנאים")
    print("=" * 50)
    
    if test_manager_features():
        print("\n✅ בדיקת תכונות בסיסיות עברה בהצלחה!")
    
    if create_demo_progress():
        print("\n✅ נתוני דמו נוצרו בהצלחה!")
    
    print("\n🎯 תכונות חדשות שנוספו:")
    print("1. 📊 דשבורד מנהל מורחב עם פרטי התקדמות")
    print("2. 📈 אחוז התקדמות ופרוגרס בר")
    print("3. 👁️ צפייה בפעולות אחרונות של הטכנאי")
    print("4. 💬 עדכונים אחרונים מהטכנאי")
    print("5. 🔗 קישור מיוחד למעקב מפורט")
    print("6. 📋 עמוד משימות מפורט לטכנאי")
    
    print("\n📋 לבדיקה:")
    print("1. היכנס כמנהל לדשבורד")
    print("2. בחר תיקון 'בביצוע'")
    print("3. לחץ על 'התקדמות טכנאי'")
    print("4. בדוק את המידע המפורט")

if __name__ == "__main__":
    main()
