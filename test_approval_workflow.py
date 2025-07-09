#!/usr/bin/env python
"""
בדיקת הטופס אחרי התיקונים
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
from django.contrib.auth.models import User

def test_approval_workflow():
    print("🧪 בדיקת תהליך האישור הלקוח...")
    
    try:
        # חיפוש תיקון קיים
        repair_job = RepairJob.objects.filter(status='diagnosed').first()
        if not repair_job:
            print("❌ לא נמצא תיקון עם סטטוס 'diagnosed'")
            return
            
        print(f"✅ נמצא תיקון: {repair_job}")
        print(f"📋 פריטי תיקון: {repair_job.repair_items.count()}")
        
        # בדיקת הטופס
        form = CustomerApprovalForm(repair_job=repair_job)
        print(f"✅ הטופס נוצר בהצלחה")
        
        # סימולציה של בחירת פריטים
        available_items = list(repair_job.repair_items.all())
        if available_items:
            # בחירת הפריט הראשון
            selected_item = available_items[0]
            test_data = {
                'approved_items': [selected_item.id]
            }
            
            form_with_data = CustomerApprovalForm(repair_job=repair_job, data=test_data)
            
            if form_with_data.is_valid():
                print("✅ הטופס תקין עם נתונים")
                approved = form_with_data.cleaned_data['approved_items']
                print(f"📝 פריטים מאושרים: {[item.description for item in approved]}")
                
                # עדכון פריטים בדומה לוויו
                for item in repair_job.repair_items.all():
                    was_approved = item.is_approved_by_customer
                    item.is_approved_by_customer = item in approved
                    if was_approved != item.is_approved_by_customer:
                        print(f"🔄 פריט '{item.description}': {was_approved} -> {item.is_approved_by_customer}")
                
                print("✅ הטופס עובד כשורה!")
            else:
                print("❌ הטופס לא תקין:", form_with_data.errors)
        else:
            print("⚠️ אין פריטי תיקון לבדיקה")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_approval_workflow()
