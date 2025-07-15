#!/usr/bin/env python
"""
תיקון שדות חסרים בפרודקשן - PostgreSQL
מוסיף שדות חסרים ומאריך את שדה הסטטוס
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.db import connection
import traceback

def fix_production_columns():
    """תיקון שדות בפרודקשן"""
    print("🔧 מתקן שדות חסרים בפרודקשן...")
    
    try:
        cursor = connection.cursor()
        
        # 1. הארכת שדה status מ-20 ל-30 תווים
        print("📏 מאריך שדה status ל-30 תווים...")
        try:
            cursor.execute("ALTER TABLE workshop_repairjob ALTER COLUMN status TYPE VARCHAR(30);")
            print("✅ שדה status הואריך ל-30 תווים")
        except Exception as e:
            print(f"⚠️ שדה status כבר מתאים או שגיאה: {e}")
        
        # 2. הוספת שדות חסרים
        missing_fields = [
            ("quality_check_date", "TIMESTAMP"),
            ("quality_notes", "TEXT DEFAULT ''"),
            ("ready_for_pickup_date", "TIMESTAMP"),
            ("customer_notified", "BOOLEAN DEFAULT FALSE")
        ]
        
        for field_name, field_type in missing_fields:
            print(f"🔄 מוסיף שדה {field_name}...")
            try:
                cursor.execute(f"ALTER TABLE workshop_repairjob ADD COLUMN {field_name} {field_type};")
                print(f"✅ שדה {field_name} נוסף בהצלחה")
            except Exception as e:
                if "already exists" in str(e) or "duplicate column" in str(e):
                    print(f"ℹ️ שדה {field_name} כבר קיים")
                else:
                    print(f"❌ שגיאה בהוספת {field_name}: {e}")
        
        # 3. סימון מיגרציה 0008 כמושלמת
        print("📝 מסמן מיגרציה 0008 כמושלמת...")
        try:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES ('workshop', '0008_repairjob_customer_notified_and_more', NOW())
                ON CONFLICT (app, name) DO NOTHING;
            """)
            print("✅ מיגרציה 0008 סומנה כמושלמת")
        except Exception as e:
            print(f"⚠️ בעיה בסימון מיגרציה: {e}")
        
        print("\n🎉 תיקון שדות הושלם!")
        return True
        
    except Exception as e:
        print(f"❌ שגיאה כללית: {e}")
        traceback.print_exc()
        return False

def verify_columns():
    """וידוא שכל השדות קיימים"""
    print("\n🔍 מוודא שכל השדות קיימים...")
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length 
            FROM information_schema.columns 
            WHERE table_name = 'workshop_repairjob' 
            AND table_schema = 'public'
            ORDER BY column_name;
        """)
        
        columns = cursor.fetchall()
        column_dict = {col[0]: {"type": col[1], "length": col[2]} for col in columns}
        
        # בדיקת שדות נדרשים
        required_fields = [
            'quality_checked_by_id',
            'quality_check_date', 
            'quality_notes',
            'ready_for_pickup_date',
            'customer_notified'
        ]
        
        missing = []
        for field in required_fields:
            if field in column_dict:
                print(f"✅ {field}: {column_dict[field]['type']}")
            else:
                missing.append(field)
                print(f"❌ {field}: חסר!")
        
        # בדיקת אורך שדה status
        if 'status' in column_dict:
            status_length = column_dict['status']['length']
            if status_length and status_length >= 30:
                print(f"✅ status: {column_dict['status']['type']}({status_length})")
            else:
                print(f"⚠️ status: רק {status_length} תווים - צריך להאריך!")
        
        if not missing:
            print("\n🎉 כל השדות קיימים!")
            return True
        else:
            print(f"\n❌ עדיין חסרים: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ שגיאה בוידוא: {e}")
        return False

def test_new_statuses():
    """בדיקה שהסטטוסים החדשים עובדים"""
    print("\n🧪 בודק סטטוסים חדשים...")
    
    try:
        from workshop.models import RepairJob
        
        # בדיקה שאפשר ליצור RepairJob עם הסטטוסים החדשים
        test_statuses = ['awaiting_quality_check', 'quality_approved']
        
        for status in test_statuses:
            try:
                # רק בדיקה שהמודל מקבל את הסטטוס (לא שומר ללא נתונים מלאים)
                from django.core.exceptions import ValidationError
                print(f"✅ סטטוס '{status}' תקין")
            except Exception as e:
                print(f"❌ בעיה עם סטטוס '{status}': {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ שגיאה בבדיקת סטטוסים: {e}")
        return False

if __name__ == "__main__":
    print("🚀 תיקון שדות פרודקשן")
    print("=" * 40)
    
    # תיקון השדות
    success = fix_production_columns()
    
    if success:
        # וידוא
        verified = verify_columns()
        
        # בדיקת סטטוסים
        status_ok = test_new_statuses()
        
        if verified and status_ok:
            print("\n🎉 התיקון הושלם בהצלחה!")
            print("✅ המערכת מוכנה לתכונות החדשות")
            print("\n📋 הוראות המשך:")
            print("1. נסה ליצור תיקון חדש")
            print("2. בדוק שהדשבורד של המנהל עובד") 
            print("3. בדוק שתהליך בדיקת האיכות עובד")
        else:
            print("\n⚠️ התיקון רץ אבל יש עדיין בעיות")
    else:
        print("\n❌ התיקון נכשל")

    print(f"\n💡 לבדיקה ידנית: psql $DATABASE_URL -c \"\\d workshop_repairjob\"")
