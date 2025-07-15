#!/usr/bin/env python
"""
יצירת נתוני דמו לבדיקת מחזור האיכות החדש
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from workshop.models import RepairJob, Customer, Bike, User, RepairItem
from django.utils import timezone

def create_quality_check_demo():
    """יצירת נתוני דמו למחזור בדיקת האיכות"""
    print("🧪 יוצר נתוני דמו למחזור בדיקת איכות...")
    
    # מציאת לקוח ואופניים
    customer = Customer.objects.first()
    if not customer:
        print("❌ לא נמצא לקוח במערכת")
        return
    
    bike = customer.bikes.first()
    if not bike:
        print("❌ לא נמצאו אופניים ללקוח")
        return
    
    # מציאת מכונאי
    mechanic = User.objects.filter(userprofile__role='mechanic').first()
    if not mechanic:
        print("❌ לא נמצא מכונאי במערכת")
        return
    
    # יצירת תיקון חדש ממתין לבדיקת איכות
    repair_awaiting_quality = RepairJob.objects.create(
        bike=bike,
        problem_description="תיקון דמו - ממתין לבדיקת איכות מנהל",
        status='awaiting_quality_check',
        assigned_mechanic=mechanic,
        diagnosis='הוחלפו בלמים וצמיגים, כוונו הילוכים',
        approved_at=timezone.now()
    )
    
    # הוספת פעולות שהושלמו
    RepairItem.objects.create(
        repair_job=repair_awaiting_quality,
        description="החלפת בלמים קדמיים ואחוריים",
        price=200.00,
        is_approved_by_customer=True,
        status='completed',
        completed_by=mechanic,
        completed_at=timezone.now(),
        notes="הותקנו בלמים איכותיים מחברת Shimano"
    )
    
    RepairItem.objects.create(
        repair_job=repair_awaiting_quality,
        description="החלפת צמיגים קדמיים ואחוריים",
        price=150.00,
        is_approved_by_customer=True,
        status='completed',
        completed_by=mechanic,
        completed_at=timezone.now(),
        notes="הותקנו צמיגים מחברת Continental"
    )
    
    RepairItem.objects.create(
        repair_job=repair_awaiting_quality,
        description="כיוון הילוכים ובדיקת שרשרת",
        price=80.00,
        is_approved_by_customer=True,
        status='completed',
        completed_by=mechanic,
        completed_at=timezone.now(),
        notes="הילוכים מכוונים בצורה מושלמת"
    )
    
    print(f"✅ נוצר תיקון #{repair_awaiting_quality.id} ממתין לבדיקת איכות")
    
    # יצירת תיקון נוסף שכבר עבר בדיקת איכות ומוכן לאיסוף
    repair_ready_pickup = RepairJob.objects.create(
        bike=bike,
        problem_description="תיקון דמו - מוכן לאיסוף אחרי בדיקת איכות",
        status='quality_approved',
        assigned_mechanic=mechanic,
        diagnosis='תיקון בלמים בלבד',
        approved_at=timezone.now(),
        quality_checked_by=User.objects.filter(userprofile__role='manager').first(),
        quality_check_date=timezone.now(),
        quality_notes="איכות מעולה! כל הפעולות בוצעו בצורה מושלמת",
        ready_for_pickup_date=timezone.now()
    )
    
    RepairItem.objects.create(
        repair_job=repair_ready_pickup,
        description="תיקון בלמים קדמיים",
        price=100.00,
        is_approved_by_customer=True,
        status='completed',
        completed_by=mechanic,
        completed_at=timezone.now(),
        notes="בלמים תוקנו ונבדקו"
    )
    
    print(f"✅ נוצר תיקון #{repair_ready_pickup.id} מוכן לאיסוף")
    
    print("\n📊 סיכום נתוני דמו חדשים:")
    print(f"🔍 תיקונים ממתינים לבדיקת איכות: {RepairJob.objects.filter(status='awaiting_quality_check').count()}")
    print(f"✅ תיקונים מוכנים לאיסוף: {RepairJob.objects.filter(status='quality_approved').count()}")
    print(f"📦 תיקונים שנמסרו: {RepairJob.objects.filter(status='delivered').count()}")
    
    print("\n🎉 נתוני דמו למחזור בדיקת איכות נוצרו בהצלחה!")
    print("💡 עכשיו לך לדשבורד המנהל ותראה את הקטגוריות החדשות")

if __name__ == "__main__":
    create_quality_check_demo()
