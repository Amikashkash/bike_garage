#!/usr/bin/env python
"""
טסט קטן לבדיקת טופס אישור הלקוח
"""
import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from workshop.models import RepairJob, RepairItem, Customer, Bike
from workshop.forms import CustomerApprovalForm

def test_customer_approval_form():
    print("🔍 בדיקת טופס אישור לקוח...")
    
    try:
        # יצירת נתונים לדוגמה (אם לא קיימים)
        customer, _ = Customer.objects.get_or_create(
            name="לקוח לבדיקה",
            phone="050-1234567",
            defaults={'email': 'test@example.com'}
        )
        
        bike, _ = Bike.objects.get_or_create(
            customer=customer,
            brand="Trek",
            defaults={'model': 'FX 3', 'color': 'כחול'}
        )
        
        repair_job, _ = RepairJob.objects.get_or_create(
            bike=bike,
            problem_description="בדיקת טופס",
            defaults={
                'status': 'diagnosed',
                'diagnosis': 'נדרש תיקון בלמים'
            }
        )
        
        # יצירת פריטי תיקון
        item1, _ = RepairItem.objects.get_or_create(
            repair_job=repair_job,
            description="החלפת בלמים",
            defaults={'price': 150.00}
        )
        item2, _ = RepairItem.objects.get_or_create(
            repair_job=repair_job,
            description="כוונון הילוכים",
            defaults={'price': 80.00}
        )
        
        print(f"✅ נוצר תיקון עם {repair_job.repair_items.count()} פריטים")
        
        # בדיקת הטופס
        form = CustomerApprovalForm(repair_job=repair_job)
        print(f"✅ הטופס נוצר בהצלחה")
        print(f"📝 שדות זמינים: {list(form.fields.keys())}")
        print(f"🔧 פריטי תיקון זמינים: {form.fields['approved_items'].queryset.count()}")
        
        # בדיקת טופס עם נתונים
        test_data = {
            'approved_items': [item1.id]  # אישור רק הפריט הראשון
        }
        form_with_data = CustomerApprovalForm(repair_job=repair_job, data=test_data)
        
        if form_with_data.is_valid():
            print("✅ הטופס תקין עם נתונים")
            approved = form_with_data.cleaned_data['approved_items']
            print(f"📋 פריטים מאושרים: {[item.description for item in approved]}")
        else:
            print("❌ הטופס לא תקין:", form_with_data.errors)
        
        print("\n🎯 הטופס מוכן לשימוש!")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_customer_approval_form()
