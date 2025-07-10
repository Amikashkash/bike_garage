#!/usr/bin/env python
"""
בדיקת תיקוני דשבורד מנהל וגישה למשימות מכונאי
"""

import os
import sys
import django

# הגדרת Django
sys.path.append('c:\\bikegarage')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import RepairJob, RepairItem, UserProfile

def test_manager_permissions():
    print("=== בדיקת הרשאות מנהל ===")
    
    # איתור מנהל וטכנאי
    try:
        manager = User.objects.filter(userprofile__role='manager').first()
        mechanic = User.objects.filter(userprofile__role='mechanic').first()
        
        if not manager:
            print("❌ לא נמצא מנהל במערכת")
            return
            
        if not mechanic:
            print("❌ לא נמצא טכנאי במערכת")
            return
            
        print(f"✅ מנהל: {manager.username}")
        print(f"✅ טכנאי: {mechanic.username}")
        
        # בדיקת תיקונים בביצוע
        in_progress = RepairJob.objects.filter(
            status__in=['approved', 'in_progress'],
            assigned_mechanic=mechanic
        ).first()
        
        if not in_progress:
            print("❌ לא נמצא תיקון בביצוע")
            return
            
        print(f"✅ תיקון בביצוע: {in_progress}")
        
        # בדיקת הערות מכונאי
        items_with_notes = in_progress.repair_items.filter(
            is_approved_by_customer=True
        ).exclude(
            notes__exact='', block_notes__exact=''
        )
        
        print(f"📝 פעולות עם הערות: {items_with_notes.count()}")
        for item in items_with_notes:
            print(f"   🔧 {item.description}")
            if item.block_notes:
                print(f"      ⚠️ חסימה: {item.block_notes}")
            if item.notes:
                print(f"      💬 הערות: {item.notes}")
                
        # בדיקת גישה למשימות מכונאי
        print(f"\n🔐 בדיקת הרשאות:")
        print(f"   URL למשימות: /mechanic/task/{in_progress.id}/")
        print(f"   מנהל יכול לגשת: {'✅ כן' if manager.userprofile.role == 'manager' else '❌ לא'}")
        
        # הדמיית context של דשבורד מנהל
        repair = in_progress
        repair.approved_items = repair.repair_items.filter(is_approved_by_customer=True)
        repair.completed_items = repair.repair_items.filter(is_approved_by_customer=True, is_completed=True)
        repair.pending_items = repair.repair_items.filter(is_approved_by_customer=True, is_completed=False)
        repair.progress_percentage = (repair.completed_items.count() / repair.approved_items.count() * 100) if repair.approved_items.count() > 0 else 0
        
        # הערות מכונאי
        repair.mechanic_notes = repair.repair_items.filter(
            is_approved_by_customer=True,
        ).exclude(
            notes__exact='', block_notes__exact=''
        ).order_by('-id')[:3]
        
        print(f"\n📊 מה המנהל יראה בדשבורד:")
        print(f"   התקדמות: {repair.progress_percentage:.0f}%")
        print(f"   פעולות מושלמות: {repair.completed_items.count()}")
        print(f"   פעולות ממתינות: {repair.pending_items.count()}")
        print(f"   הערות מכונאי: {repair.mechanic_notes.count()}")
        
        for note in repair.mechanic_notes:
            if note.is_blocked:
                print(f"      🚫 חסום: {note.block_notes[:40]}...")
            elif note.notes:
                print(f"      💬 הערה: {note.notes[:40]}...")
                
        print(f"\n🌐 קישורים לבדיקה:")
        print(f"   דשבורד מנהל: http://localhost:8000/manager/")
        print(f"   משימות מכונאי: http://localhost:8000/mechanic/task/{in_progress.id}/")
        print(f"   התחבר כ: {manager.username}")
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_manager_permissions()
