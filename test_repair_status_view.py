#!/usr/bin/env python3
"""
סקריפט ליצירת נתוני דמו ובדיקת תצוגת repair_status
"""

import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from workshop.models import RepairJob, RepairItem, Bike, Customer, WorkshopUser
from django.contrib.auth.models import User

def create_test_data():
    """יוצר נתוני דמו לבדיקת תצוגת repair_status"""
    print("🔧 יוצר נתוני דמו לבדיקת תצוגת repair_status...")
    
    # יצירת משתמש/לקוח
    try:
        user = User.objects.get(username='test_customer')
        print(f"✅ משתמש קיים: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='test_customer',
            password='123',
            first_name='יוסי',
            last_name='כהן'
        )
        print(f"✅ נוצר משתמש חדש: {user.username}")
    
    # יצירת לקוח
    try:
        customer = Customer.objects.get(user=user)
        print(f"✅ לקוח קיים: {customer.name}")
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=user,
            name='יוסי כהן',
            phone='052-1234567',
            email='yossi@test.com'
        )
        print(f"✅ נוצר לקוח חדש: {customer.name}")
    
    # יצירת אופניים
    try:
        bike = Bike.objects.get(customer=customer)
        print(f"✅ אופניים קיימים: {bike}")
    except Bike.DoesNotExist:
        bike = Bike.objects.create(
            customer=customer,
            brand='Trek',
            model='X-Caliber 8',
            year=2022,
            color='כחול'
        )
        print(f"✅ נוצרו אופניים חדשים: {bike}")
    
    # יצירת מכונאי
    try:
        mechanic_user = User.objects.get(username='mechanic1')
        print(f"✅ מכונאי קיים: {mechanic_user.username}")
    except User.DoesNotExist:
        mechanic_user = User.objects.create_user(
            username='mechanic1',
            password='123',
            first_name='דני',
            last_name='המכונאי'
        )
        print(f"✅ נוצר מכונאי חדש: {mechanic_user.username}")
    
    try:
        mechanic = WorkshopUser.objects.get(user=mechanic_user)
        mechanic.role = 'mechanic'
        mechanic.save()
        print(f"✅ מכונאי WorkshopUser קיים: {mechanic}")
    except WorkshopUser.DoesNotExist:
        mechanic = WorkshopUser.objects.create(
            user=mechanic_user,
            role='mechanic'
        )
        print(f"✅ נוצר WorkshopUser מכונאי חדש: {mechanic}")
    
    # יצירת תיקון
    try:
        repair_job = RepairJob.objects.get(bike=bike)
        print(f"✅ תיקון קיים: #{repair_job.id}")
    except RepairJob.DoesNotExist:
        repair_job = RepairJob.objects.create(
            bike=bike,
            problem_description='בעיה בהילוכים - לא עוברים כהלכה, שרשרת קופצת',
            status='in_progress',
            assigned_mechanic=mechanic,
            diagnosis='נדרש החלפת כבל הילוכים וכיוונון מחדש'
        )
        print(f"✅ נוצר תיקון חדש: #{repair_job.id}")
    
    # מחיקת פריטים קיימים
    RepairItem.objects.filter(repair_job=repair_job).delete()
    print("🗑️ נמחקו פריטי תיקון קיימים")
    
    # יצירת פריטי תיקון עם הערות שונות
    items_data = [
        {
            'description': 'החלפת כבל הילוכים אחורי',
            'price': 80,
            'is_approved_by_customer': True,
            'is_completed': True,
            'notes': 'הכבל היה שחוק מאוד. הוחלף בכבל איכותי מסוג Shimano. הבדיקה הראתה שיפור משמעותי בתפקוד ההילוכים.'
        },
        {
            'description': 'כיוונון מערכת הילוכים',
            'price': 50,
            'is_approved_by_customer': True,
            'is_completed': True,
            'notes': 'בוצע כיוונון מדויק של כל ההילוכים. נבדקו כל המעברים והושגה רמת דיוק גבוהה.'
        },
        {
            'description': 'בדיקת מערכת בלמים',
            'price': 30,
            'is_approved_by_customer': True,
            'is_completed': False,
            'notes': 'זוהתה בעיה בלוחיות הבלם האחוריות - דרוש החלפה. ממליץ על החלפה מיידית מטעמי בטיחות!'
        },
        {
            'description': 'החלפת לוחיות בלם אחוריות',
            'price': 120,
            'is_approved_by_customer': False,
            'is_completed': False,
            'notes': 'לוחיות הבלם בלויות מעבר למותר. החלפה דחופה נדרשת לפני רכיבה נוספת.'
        },
        {
            'description': 'שמן וניקוי שרשרת',
            'price': 25,
            'is_approved_by_customer': True,
            'is_completed': True,
            'notes': 'שרשרת נוקתה בקפידה ושומנה בשמן איכותי. מומלץ על שמון חוזר כל 200 ק"מ.'
        }
    ]
    
    for item_data in items_data:
        item = RepairItem.objects.create(
            repair_job=repair_job,
            description=item_data['description'],
            price=item_data['price'],
            is_approved_by_customer=item_data['is_approved_by_customer'],
            is_completed=item_data['is_completed'],
            notes=item_data['notes']
        )
        
        if item_data['is_completed']:
            item.completed_by = mechanic
            item.save()
        
        print(f"✅ נוצר פריט: {item.description} - הערה: {item.notes[:30]}...")
    
    print(f"\n🎯 נוצרו {len(items_data)} פריטי תיקון עם הערות")
    print(f"📋 תיקון #{repair_job.id} מוכן לבדיקה")
    print(f"🌐 URL לבדיקה: http://127.0.0.1:8000/repair/{repair_job.id}/")
    
    return repair_job

def show_repair_status():
    """מציג את סטטוס התיקון"""
    try:
        repair_job = RepairJob.objects.first()
        if not repair_job:
            print("❌ לא נמצא תיקון")
            return
        
        print(f"\n📋 תיקון #{repair_job.id} - {repair_job.bike.customer.name}")
        print(f"🚲 אופניים: {repair_job.bike}")
        print(f"📊 סטטוס: {repair_job.get_status_display()}")
        
        if repair_job.assigned_mechanic:
            print(f"🔧 מכונאי: {repair_job.assigned_mechanic.user.get_full_name()}")
        
        print(f"\n🛠️ פריטי תיקון ({repair_job.repair_items.count()}):")
        for item in repair_job.repair_items.all():
            status = "✅ הושלם" if item.is_completed else ("⏳ מאושר" if item.is_approved_by_customer else "❓ ממתין לאישור")
            print(f"  {status} {item.description} - ₪{item.price}")
            if item.notes:
                print(f"    💬 הערה: {item.notes}")
                
        print(f"\n💰 סה\"כ מאושר: ₪{repair_job.get_total_approved_price()}")
        print(f"⏳ ממתין לאישור: ₪{repair_job.get_pending_approval_price()}")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")

if __name__ == "__main__":
    print("🚀 בדיקת תצוגת repair_status")
    print("=" * 50)
    
    repair_job = create_test_data()
    show_repair_status()
    
    print("\n" + "=" * 50)
    print("✅ הדמו מוכן!")
    print(f"🌐 בדוק בדפדפן: http://127.0.0.1:8000/repair/{repair_job.id}/")
