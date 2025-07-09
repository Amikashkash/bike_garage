#!/usr/bin/env python
"""
בדיקה מהירה של הטופס
"""
import os
import sys
import django

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from workshop.models import RepairJob
from workshop.forms import CustomerApprovalForm

def test_form():
    print("🧪 בדיקה מהירה של הטופס...")
    
    # חיפוש תיקון
    try:
        repair = RepairJob.objects.get(id=5)
        print(f"✅ נמצא תיקון: {repair}")
        print(f"📋 פריטים: {repair.repair_items.count()}")
        
        if repair.repair_items.count() == 0:
            print("❌ אין פריטי תיקון!")
            return
            
        # יצירת טופס
        form = CustomerApprovalForm(repair_job=repair)
        print(f"✅ טופס נוצר בהצלחה")
        print(f"🔧 שדות: {list(form.fields.keys())}")
        
        # בדיקה עם נתונים
        first_item = repair.repair_items.first()
        test_data = {'approved_items': [first_item.id]}
        
        form_with_data = CustomerApprovalForm(repair_job=repair, data=test_data)
        print(f"📝 טופס עם נתונים תקין: {form_with_data.is_valid()}")
        
        if form_with_data.is_valid():
            print(f"✅ נתונים נקלטו: {[item.description for item in form_with_data.cleaned_data['approved_items']]}")
        else:
            print(f"❌ שגיאות: {form_with_data.errors}")
            
    except RepairJob.DoesNotExist:
        print("❌ לא נמצא תיקון עם ID 5")
        print("💡 נוצר תיקון חדש...")
        # יצירת תיקון לבדיקה
        from workshop.management.commands.create_test_approval import Command
        cmd = Command()
        cmd.handle()
        print("✅ נוצר תיקון לבדיקה")

if __name__ == "__main__":
    test_form()
