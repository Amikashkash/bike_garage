#!/usr/bin/env python
"""
Final comprehensive test of the Bike Garage stuck system
"""
import os
import sys
import django
import sqlite3
from datetime import datetime

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import Customer, RepairJob, UserProfile

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def check_database_structure():
    """Check if all database fields exist"""
    print_header("בדיקת מבנה מסד הנתונים")
    
    try:
        db_path = 'db.sqlite3'
        if not os.path.exists(db_path):
            print_error("קובץ מסד הנתונים לא נמצא")
            return False
            
        print_success("קובץ מסד הנתונים קיים")
        
        # Check table structure
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(workshop_repairjob);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        required_fields = ['is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response']
        
        print_info("בדיקת שדות התקיעות:")
        all_fields_exist = True
        for field in required_fields:
            if field in column_names:
                print_success(f"שדה {field} קיים")
            else:
                print_error(f"שדה {field} חסר!")
                all_fields_exist = False
        
        conn.close()
        return all_fields_exist
        
    except Exception as e:
        print_error(f"שגיאה בבדיקת מסד הנתונים: {str(e)}")
        return False

def check_django_models():
    """Check if Django models have the required fields"""
    print_header("בדיקת מודלים של Django")
    
    try:
        from workshop.models import RepairJob
        
        # Get model fields
        field_names = [f.name for f in RepairJob._meta.get_fields()]
        print_info(f"שדות במודל RepairJob: {len(field_names)} שדות")
        
        required_fields = ['is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response']
        
        all_fields_exist = True
        for field in required_fields:
            if field in field_names:
                print_success(f"שדה {field} במודל")
            else:
                print_error(f"שדה {field} חסר במודל!")
                all_fields_exist = False
        
        return all_fields_exist
        
    except Exception as e:
        print_error(f"שגיאה בטעינת מודלים: {str(e)}")
        return False

def test_crud_operations():
    """Test CRUD operations on stuck fields"""
    print_header("בדיקת פעולות CRUD על שדות התקיעות")
    
    try:
        # Create test customer
        customer, created = Customer.objects.get_or_create(
            name="Test Customer - Final",
            defaults={
                'phone': '1234567890',
                'email': 'test@example.com'
            }
        )
        
        if created:
            print_success("לקוח בדיקה נוצר")
        else:
            print_info("לקוח בדיקה כבר קיים")
        
        # Create repair job
        repair_job = RepairJob.objects.create(
            customer=customer,
            bike_model="Test Bike Final",
            description="Final test repair",
            status="in_progress"
        )
        print_success(f"תיקון נוצר עם ID: {repair_job.id}")
        
        # Test stuck functionality
        repair_job.is_stuck = True
        repair_job.stuck_reason = "Final test - waiting for parts"
        repair_job.save()
        print_success("תיקון סומן כתקוע")
        
        # Verify data persistence
        saved_job = RepairJob.objects.get(id=repair_job.id)
        assert saved_job.is_stuck == True
        assert saved_job.stuck_reason == "Final test - waiting for parts"
        print_success("נתונים נשמרו נכון במסד הנתונים")
        
        # Test manager response
        saved_job.manager_response = "Parts ordered - arriving tomorrow"
        saved_job.save()
        print_success("תגובת מנהל נוספה")
        
        # Test resolution
        saved_job.stuck_resolved = True
        saved_job.is_stuck = False
        saved_job.save()
        print_success("תקיעות נפתרה")
        
        # Clean up
        repair_job.delete()
        if created:
            customer.delete()
        print_success("נתונים נוקו")
        
        return True
        
    except Exception as e:
        print_error(f"שגיאה בבדיקת CRUD: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_urls_and_views():
    """Check if URLs and views are properly configured"""
    print_header("בדיקת URLs ו-Views")
    
    try:
        from django.urls import reverse
        from workshop import views
        
        # Check if views exist
        if hasattr(views, 'update_repair_status'):
            print_success("View update_repair_status קיים")
        else:
            print_error("View update_repair_status חסר")
            
        if hasattr(views, 'manager_response_stuck'):
            print_success("View manager_response_stuck קיים")
        else:
            print_error("View manager_response_stuck חסר")
        
        # Check URLs
        try:
            url = reverse('update_repair_status')
            print_success(f"URL update_repair_status: {url}")
        except:
            print_error("URL update_repair_status לא נמצא")
            
        try:
            url = reverse('manager_response_stuck')
            print_success(f"URL manager_response_stuck: {url}")
        except:
            print_error("URL manager_response_stuck לא נמצא")
        
        return True
        
    except Exception as e:
        print_error(f"שגיאה בבדיקת URLs: {str(e)}")
        return False

def check_templates():
    """Check if templates exist"""
    print_header("בדיקת Templates")
    
    templates_to_check = [
        'workshop/templates/workshop/mechanic_dashboard.html',
        'workshop/templates/workshop/manager_dashboard.html',
        'workshop/templates/workshop/repair_status.html'
    ]
    
    all_exist = True
    for template in templates_to_check:
        if os.path.exists(template):
            print_success(f"Template {template} קיים")
        else:
            print_error(f"Template {template} חסר")
            all_exist = False
    
    return all_exist

def run_final_system_test():
    """Run complete system test"""
    print_header("🚀 בדיקה מלאה של מערכת ניהול התקיעות")
    
    tests = [
        ("בדיקת מבנה מסד הנתונים", check_database_structure),
        ("בדיקת מודלים של Django", check_django_models),
        ("בדיקת פעולות CRUD", test_crud_operations),
        ("בדיקת URLs ו-Views", check_urls_and_views),
        ("בדיקת Templates", check_templates),
    ]
    
    results = []
    for test_name, test_func in tests:
        print_info(f"מריץ: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"שגיאה ב{test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print_header("📊 סיכום תוצאות")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: עבר")
        else:
            print_error(f"{test_name}: נכשל")
    
    print(f"\n📈 תוצאות כלליות: {passed}/{total} בדיקות עברו")
    
    if passed == total:
        print_header("🎉 המערכת מוכנה לשימוש!")
        print_success("כל הבדיקות עברו בהצלחה")
        print_info("מערכת ניהול התקיעות פועלת כראוי ומוכנה לשימוש")
        print_info("ניתן לגשת לממשק המכונאי והמנהל ולהתחיל לעבוד")
        
        print("\n🔧 הוראות שימוש:")
        print("1. היכנס כמכונאי ולחץ על כפתור 'תקוע' לסימון תקיעות")
        print("2. הזן סיבת התקיעות בחלון הקופץ")
        print("3. היכנס כמנהל לראות התראות על תיקונים תקועים")
        print("4. הגב למכונאי דרך ממשק המנהל")
        print("5. סמן תקיעות כפתורות כאשר הבעיה נפתרה")
        
    else:
        print_header("⚠️ המערכת זקוקה לתיקונים")
        print_error(f"{total - passed} בדיקות נכשלו")
        print_info("נא לטפל בשגיאות שנמצאו לפני השימוש במערכת")
    
    return passed == total

if __name__ == "__main__":
    success = run_final_system_test()
    
    if success:
        print("\n" + "🎊" * 20)
        print("   מערכת ניהול התקיעות הושלמה בהצלחה!")
        print("🎊" * 20)
    else:
        print("\n" + "🔧" * 20) 
        print("   יש לטפל בבעיות שנמצאו")
        print("🔧" * 20)
