#!/usr/bin/env python
"""
סקריפט ליצירת נתוני דמו לדשבורד מנהל
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, Customer, Bike, User, RepairCategory, RepairSubCategory, RepairItem
from django.contrib.auth.models import Group
from django.utils import timezone
import random

def create_dashboard_demo_data():
    print("🧪 יוצר נתוני דמו לדשבורד מנהל...")
    
    # מציאת לקוח קיים או יצירת חדש
    customer = Customer.objects.first()
    if not customer:
        print("⚠️ לא נמצא לקוח במערכת")
        return
    
    # מציאת אופניים קיימות או יצירת חדשות
    bike = Bike.objects.filter(customer=customer).first()
    if not bike:
        bike = Bike.objects.create(
            customer=customer,
            brand="דמו",
            model="בדיקות דשבורד",
            color="כחול"
        )
        print(f"✅ אופניים נוצרו: {bike}")
    
    # מציאת מכונאי
    mechanic = User.objects.filter(groups__name='Mechanics').first()
    if not mechanic:
        print("⚠️ לא נמצא מכונאי במערכת - ניסיון ליצור...")
        # ניסיון ליצור מכונאי בסיסי
        try:
            mechanic = User.objects.create_user(
                username="demo_mechanic",
                password="1234",
                first_name="מכונאי",
                last_name="דמו"
            )
            mechanics_group, _ = Group.objects.get_or_create(name='Mechanics')
            mechanic.groups.add(mechanics_group)
            print(f"✅ מכונאי נוצר: {mechanic.username}")
        except:
            print("❌ לא הצלחתי ליצור מכונאי")
            mechanic = None
    
    # מחיקת תיקונים דמו קיימים
    RepairJob.objects.filter(problem_description__contains="דמו").delete()
    print("🗑️ תיקוני דמו קיימים נמחקו")
    
    # יצירת תיקונים בסטטוסים שונים
    repairs_to_create = [
        {
            'status': 'reported',
            'description': 'תקלה דמו - דווחה על ידי לקוח',
            'mechanic': None
        },
        {
            'status': 'diagnosed', 
            'description': 'תקלה דמו - מאובחנת ממתינה לאישור',
            'mechanic': None,
            'diagnosis': 'יש צורך בהחלפת בלמים קדמיים - ₪150'
        },
        {
            'status': 'partially_approved',
            'description': 'תקלה דמו - אושרה חלקית',
            'mechanic': mechanic
        },
        {
            'status': 'approved',
            'description': 'תקלה דמו - מאושרת ממתינה להתחלה',
            'mechanic': mechanic,
            'approved_at': timezone.now()
        },
        {
            'status': 'in_progress',
            'description': 'תקלה דמו - בביצוע כרגע',
            'mechanic': mechanic,
            'approved_at': timezone.now()
        },
        {
            'status': 'in_progress',
            'description': 'תקלה דמו - תקועה!',
            'mechanic': mechanic,
            'approved_at': timezone.now(),
            'is_stuck': True,
            'stuck_reason': 'חסר חלק במחסן - צריך להזמין בלם אחורי',
            'stuck_at': timezone.now()
        }
    ]
    
    created_count = 0
    for repair_data in repairs_to_create:
        repair = RepairJob.objects.create(
            bike=bike,
            problem_description=repair_data['description'],
            status=repair_data['status'],
            assigned_mechanic=repair_data['mechanic'],
            diagnosis=repair_data.get('diagnosis', ''),
            approved_at=repair_data.get('approved_at'),
            is_stuck=repair_data.get('is_stuck', False),
            stuck_reason=repair_data.get('stuck_reason', ''),
            stuck_at=repair_data.get('stuck_at')
        )
        
        # הוספת פעולות תיקון לתיקונים שצריכים אותן
        if repair.status in ['approved', 'in_progress']:
            # יצירת פעולות דמו
            item1 = RepairItem.objects.create(
                repair_job=repair,
                description="בדיקת בלמים",
                price=50.00,
                is_approved_by_customer=True,
                status='completed' if repair.status == 'in_progress' and not repair.is_stuck else 'pending'
            )
            
            item2 = RepairItem.objects.create(
                repair_job=repair,
                description="החלפת צמיג אחורי",
                price=120.00,
                is_approved_by_customer=True,
                status='blocked' if repair.is_stuck else 'pending'
            )
            
            if not repair.is_stuck:
                item3 = RepairItem.objects.create(
                    repair_job=repair,
                    description="כיוון הילוכים",
                    price=80.00,
                    is_approved_by_customer=True,
                    status='pending'
                )
            else:
                # לתיקון תקוע - נוסיף פעולה שהושלמה ופעולה חסומה
                item3 = RepairItem.objects.create(
                    repair_job=repair,
                    description="ניקוי שרשרת",
                    price=30.00,
                    is_approved_by_customer=True,
                    status='completed'
                )
            
            print(f"✅ נוספו פעולות לתיקון #{repair.id}")
        
        elif repair.status == 'partially_approved':
            # גם לתיקונים מאושרים חלקית צריכות להיות פעולות
            RepairItem.objects.create(
                repair_job=repair,
                description="החלפת בלמים קדמיים",
                price=150.00,
                is_approved_by_customer=True
            )
            RepairItem.objects.create(
                repair_job=repair,
                description="החלפת בלמים אחוריים",
                price=120.00,
                is_approved_by_customer=False  # לא אושר
            )
            print(f"✅ נוספו פעולות לתיקון חלקית מאושר #{repair.id}")
            
        elif repair.status == 'diagnosed':
            # לתיקונים מאובחנים - פעולות שממתינות לאישור
            RepairItem.objects.create(
                repair_job=repair,
                description="החלפת צמיגים קדמיים ואחוריים",
                price=200.00,
                is_approved_by_customer=False
            )
            RepairItem.objects.create(
                repair_job=repair,
                description="כיוון בלמים ובדיקת כבלים",
                price=80.00,
                is_approved_by_customer=False
            )
            print(f"✅ נוספו פעולות לתיקון מאובחן #{repair.id}")
        
        created_count += 1
        print(f"✅ תיקון נוצר: {repair.status} - {repair.problem_description[:30]}...")
    
    print(f"\n📊 סיכום נתונים שנוצרו:")
    print(f"✅ {created_count} תיקונים נוצרו")
    
    # בדיקת התוצאות
    print(f"\n📈 נתונים נוכחיים במערכת:")
    print(f"🔴 דווחו: {RepairJob.objects.filter(status='reported').count()}")
    print(f"🟡 מאובחנו: {RepairJob.objects.filter(status='diagnosed').count()}")
    print(f"🟠 אושרו חלקית: {RepairJob.objects.filter(status='partially_approved').count()}")
    print(f"🟢 מאושרים: {RepairJob.objects.filter(status='approved').count()}")
    print(f"🔵 בביצוע: {RepairJob.objects.filter(status='in_progress').count()}")
    print(f"🚨 תקועים: {RepairJob.objects.filter(is_stuck=True).count()}")
    
    print("\n🎉 נתוני דמו נוצרו בהצלחה!")
    print("💡 עכשיו לך לדשבורד המנהל ותראה את הנתונים")

if __name__ == "__main__":
    create_dashboard_demo_data()
