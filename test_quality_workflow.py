#!/usr/bin/env python
"""
בדיקה מקיפה של פונקציונליות בדיקת האיכות
"""
import os
import django
from datetime import datetime

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, Customer
from django.contrib.auth.models import User

def test_quality_workflow():
    """בדיקת זרימת עבודה של בדיקת איכות"""
    print("🔧 בודק זרימת עבודה של בדיקת איכות...")
    
    try:
        # יצירת נתוני דמו לבדיקה
        print("\n1️⃣ יוצר נתוני דמו...")
        
        # וידוא שיש לנו מנהל
        manager = User.objects.filter(is_staff=True).first()
        if not manager:
            manager = User.objects.create_user(
                username='test_manager',
                email='manager@test.com',
                password='testpass123',
                is_staff=True
            )
            print("✅ נוצר משתמש מנהל")
        else:
            print("✅ מנהל קיים")
        
        # וידוא שיש לנו לקוח ואופניים
        customer = Customer.objects.first()
        if not customer:
            customer_user = User.objects.create_user(
                username='test_customer',
                email='customer@test.com',
                password='testpass123'
            )
            customer = Customer.objects.create(
                user=customer_user,
                name='לקוח בדיקה',
                phone='050-1234567',
                email='customer@test.com'
            )
            print("✅ נוצר לקוח")
        else:
            print("✅ לקוח קיים")
        
        # וידוא שיש אופניים
        from workshop.models import Bike
        bike = Bike.objects.filter(customer=customer).first()
        if not bike:
            bike = Bike.objects.create(
                customer=customer,
                brand='Giant',
                model='Mountain',
                color='שחור'
            )
            print("✅ נוצרו אופניים")
        else:
            print("✅ אופניים קיימים")
        
        # יצירת תיקון בסטטוס "בביצוע"
        repair_job = RepairJob.objects.create(
            bike=bike,
            problem_description='בדיקת זרימת עבודה של בדיקת איכות',
            status='in_progress'
        )
        print("✅ נוצר תיקון לבדיקה")
        
        # 2. מעבר לסטטוס "ממתין לבדיקת איכות"
        print("\n2️⃣ מעביר לסטטוס ממתין לבדיקת איכות...")
        repair_job.status = 'awaiting_quality_check'
        repair_job.save()
        print("✅ הסטטוס עודכן")
        
        # 3. ביצוע בדיקת איכות
        print("\n3️⃣ מבצע בדיקת איכות...")
        repair_job.quality_checked_by = manager
        repair_job.quality_check_date = datetime.now()
        repair_job.quality_notes = "התיקון בוצע בצורה מעולה"
        repair_job.status = 'quality_approved'
        repair_job.save()
        print("✅ בדיקת איכות הושלמה")
        
        # 4. סימון כמוכן לאיסוף
        print("\n4️⃣ מסמן כמוכן לאיסוף...")
        repair_job.ready_for_pickup_date = datetime.now()
        repair_job.customer_notified = True
        repair_job.save()
        print("✅ מוכן לאיסוף")
        
        # 5. בדיקת הנתונים
        print("\n5️⃣ בודק את הנתונים...")
        updated_job = RepairJob.objects.get(id=repair_job.id)
        
        print(f"סטטוס: {updated_job.status}")
        print(f"נבדק ע״י: {updated_job.quality_checked_by}")
        print(f"תאריך בדיקה: {updated_job.quality_check_date}")
        print(f"הערות איכות: {updated_job.quality_notes}")
        print(f"מוכן לאיסוף: {updated_job.ready_for_pickup_date}")
        print(f"לקוח הודע: {updated_job.customer_notified}")
        
        # 6. בדיקת דשבורד מנהל
        print("\n6️⃣ בודק דשבורד מנהל...")
        awaiting_quality = RepairJob.objects.filter(status='awaiting_quality_check').count()
        ready_for_pickup = RepairJob.objects.filter(status='quality_approved').count()
        
        print(f"ממתינים לבדיקת איכות: {awaiting_quality}")
        print(f"מוכנים לאיסוף: {ready_for_pickup}")
        
        print("\n✅ זרימת העבודה עובדת כראוי!")
        
        # ניקוי
        repair_job.delete()
        if manager.username == 'test_manager':
            manager.delete()
        if customer.user and customer.user.username == 'test_customer':
            customer.user.delete()
            
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקה: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_quality_workflow()
