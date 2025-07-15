#!/usr/bin/env python
"""
יצירת נתוני דמו מלאים למערכת מוסך האופניים
"""
import os
import django
from datetime import datetime, timedelta

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import Customer, Bike, RepairJob, RepairItem, UserProfile
from django.contrib.auth.models import User

def create_full_demo_data():
    """יצירת נתוני דמו מלאים"""
    print("🔧 יוצר נתוני דמו מלאים למערכת...")
    
    try:
        # 1. יצירת משתמשים
        print("\n1️⃣ יוצר משתמשים...")
        
        # מנהל
        manager_user, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@bikegarage.com',
                'is_staff': True,
                'is_superuser': True,
                'first_name': 'אמי',
                'last_name': 'מנהל'
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            print("✅ נוצר מנהל")
        else:
            print("✅ מנהל קיים")
        
        # מכונאי
        mechanic_user, created = User.objects.get_or_create(
            username='mechanic',
            defaults={
                'email': 'mechanic@bikegarage.com',
                'first_name': 'יוסי',
                'last_name': 'מכונאי'
            }
        )
        if created:
            mechanic_user.set_password('mechanic123')
            mechanic_user.save()
            print("✅ נוצר מכונאי")
        else:
            print("✅ מכונאי קיים")
        
        # לקוחות
        customers_data = [
            ('customer1', 'דני', 'cohen', 'dani@test.com', '050-1234567'),
            ('customer2', 'שרה', 'levi', 'sara@test.com', '052-9876543'),
            ('customer3', 'מיכל', 'israeli', 'michal@test.com', '054-5555555')
        ]
        
        customers = []
        for username, first_name, last_name, email, phone in customers_data:
            customer_user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if created:
                customer_user.set_password('customer123')
                customer_user.save()
            
            customer, created = Customer.objects.get_or_create(
                user=customer_user,
                defaults={
                    'name': f"{first_name} {last_name}",
                    'phone': phone,
                    'email': email
                }
            )
            customers.append(customer)
        
        print(f"✅ נוצרו {len(customers)} לקוחות")
        
        # 2. יצירת אופניים
        print("\n2️⃣ יוצר אופניים...")
        bikes_data = [
            (customers[0], 'Giant', 'Talon', 'שחור'),
            (customers[0], 'Trek', 'Marlin', 'כחול'),
            (customers[1], 'Cannondale', 'Trail', 'אדום'),
            (customers[2], 'Specialized', 'Rockhopper', 'לבן'),
            (customers[2], 'Scott', 'Aspect', 'ירוק')
        ]
        
        bikes = []
        for customer, brand, model, color in bikes_data:
            bike, created = Bike.objects.get_or_create(
                customer=customer,
                brand=brand,
                model=model,
                defaults={'color': color}
            )
            bikes.append(bike)
        
        print(f"✅ נוצרו {len(bikes)} אופניים")
        
        # 3. יצירת תיקונים בסטטוסים שונים
        print("\n3️⃣ יוצר תיקונים...")
        repairs_data = [
            (bikes[0], 'החלפת שרשרת', 'reported', None, 0),
            (bikes[1], 'תיקון בלמים', 'diagnosed', None, 1),
            (bikes[2], 'תיקון גלגל אחורי', 'approved', mechanic_user, 2),
            (bikes[3], 'תחזוקה כללית', 'in_progress', mechanic_user, 3),
            (bikes[4], 'החלפת צמיגים', 'awaiting_quality_check', mechanic_user, 4),
        ]
        
        created_repairs = []
        for i, (bike, problem, status, mechanic, days_ago) in enumerate(repairs_data):
            created_date = datetime.now() - timedelta(days=days_ago)
            
            repair, created = RepairJob.objects.get_or_create(
                bike=bike,
                problem_description=problem,
                defaults={
                    'status': status,
                    'assigned_mechanic': mechanic,
                    'created_at': created_date
                }
            )
            
            if created:
                repair.created_at = created_date
                repair.save()
            
            created_repairs.append(repair)
        
        print(f"✅ נוצרו {len(created_repairs)} תיקונים")
        
        # 4. הוספת תיקון שעבר בדיקת איכות
        print("\n4️⃣ יוצר תיקון שעבר בדיקת איכות...")
        quality_repair = RepairJob.objects.create(
            bike=bikes[0],
            problem_description='החלפת הילוכים - עבר בדיקת איכות',
            status='quality_approved',
            assigned_mechanic=mechanic_user,
            quality_checked_by=manager_user,
            quality_check_date=datetime.now() - timedelta(hours=2),
            quality_notes='התיקון בוצע בצורה מעולה. כל הרכיבים עובדים כראוי.',
            ready_for_pickup_date=datetime.now() - timedelta(hours=1),
            customer_notified=True
        )
        print("✅ נוצר תיקון שעבר בדיקת איכות")
        
        # 5. הצגת סיכום
        print("\n📊 סיכום נתוני הדמו:")
        print("-" * 40)
        print(f"משתמשים: {User.objects.count()}")
        print(f"לקוחות: {Customer.objects.count()}")
        print(f"אופניים: {Bike.objects.count()}")
        print(f"תיקונים: {RepairJob.objects.count()}")
        
        print(f"\nסטטוס תיקונים:")
        for status_code, status_name in RepairJob.STATUS_CHOICES:
            count = RepairJob.objects.filter(status=status_code).count()
            if count > 0:
                print(f"  {status_name}: {count}")
        
        print("\n✅ נתוני דמו נוצרו בהצלחה!")
        print("\n🔐 פרטי כניסה:")
        print("מנהל: manager / manager123")
        print("מכונאי: mechanic / mechanic123")
        print("לקוח: customer1 / customer123")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה ביצירת נתוני דמו: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_full_demo_data()
