#!/usr/bin/env python
"""
בדיקת סטטוס המערכת אחרי עדכונים
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def check_system_status():
    """בדיקה כוללת של המערכת"""
    print("🔍 בדיקת סטטוס מערכת אחרי עדכונים")
    print("=" * 50)
    
    from workshop.models import RepairJob, Customer, Bike, User
    from django.db import connection
    
    try:
        # 1. בדיקת חיבור למסד נתונים
        print("\n📊 בדיקת מסד נתונים:")
        users_count = User.objects.count()
        repairs_count = RepairJob.objects.count()
        customers_count = Customer.objects.count()
        
        print(f"   👥 משתמשים: {users_count}")
        print(f"   🔧 תיקונים: {repairs_count}")
        print(f"   🚴 לקוחות: {customers_count}")
        
        # 2. בדיקת שדות בדיקת איכות
        print("\n🔍 בדיקת שדות בדיקת איכות:")
        cursor = connection.cursor()
        cursor.execute("PRAGMA table_info(workshop_repairjob);")
        columns = [row[1] for row in cursor.fetchall()]
        
        quality_fields = [
            'quality_checked_by_id',
            'quality_check_date',
            'quality_notes',
            'ready_for_pickup_date',
            'customer_notified'
        ]
        
        all_present = True
        for field in quality_fields:
            present = field in columns
            status = "✅" if present else "❌"
            print(f"   {status} {field}")
            if not present:
                all_present = False
        
        # 3. בדיקת יצירת תיקון
        print("\n🧪 בדיקת יצירת תיקון חדש:")
        try:
            customer = Customer.objects.first()
            if customer:
                bike = customer.bikes.first()
                if bike:
                    # יצירת תיקון בדיקה
                    test_repair = RepairJob(
                        bike=bike,
                        problem_description="בדיקת מערכת",
                        status='reported'
                    )
                    test_repair.save()
                    print(f"   ✅ תיקון נוצר: #{test_repair.id}")
                    
                    # מחיקה מיידית
                    test_repair.delete()
                    print("   🗑️ תיקון בדיקה נמחק")
                else:
                    print("   ⚠️ לא נמצאו אופניים")
            else:
                print("   ⚠️ לא נמצא לקוח")
        except Exception as e:
            print(f"   ❌ שגיאה ביצירת תיקון: {e}")
            all_present = False
        
        # 4. בדיקת סטטוסים חדשים
        print("\n📈 בדיקת סטטוסים חדשים:")
        try:
            awaiting_quality = RepairJob.objects.filter(status='awaiting_quality_check').count()
            quality_approved = RepairJob.objects.filter(status='quality_approved').count()
            
            print(f"   🔍 ממתינים לבדיקת איכות: {awaiting_quality}")
            print(f"   ✅ מוכנים לאיסוף: {quality_approved}")
        except Exception as e:
            print(f"   ⚠️ בעיה בסטטוסים חדשים: {e}")
        
        # סיכום
        print(f"\n{'='*50}")
        if all_present:
            print("🎉 המערכת פועלת תקין!")
            print("✅ כל התכונות החדשות זמינות")
        else:
            print("⚠️ המערכת פועלת עם מגבלות")
            print("💡 חלק מהתכונות החדשות אינן זמינות")
            
        return all_present
        
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
        return False

if __name__ == "__main__":
    check_system_status()
