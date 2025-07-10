#!/usr/bin/env python3
"""
דף דמו לבדיקת עיצוב דשבורד מנהל - ללא הרשאות
"""

from django.shortcuts import render
from django.http import HttpResponse

def demo_manager_dashboard(request):
    """דמו דשבורד מנהל - ללא דרישת הרשאות"""
    
    # נתוני דמו
    context = {
        'pending_diagnosis': [
            {
                'id': 1,
                'bike': 'Trek X-Caliber 9',
                'bike__customer__name': 'יוסי כהן',
                'problem_description': 'בעיה בבלמים קדמיים',
                'created_at': '2025-07-10 14:30:00'
            },
            {
                'id': 2,
                'bike': 'Specialized Stumpjumper',
                'bike__customer__name': 'שרה לוי',
                'problem_description': 'החלפת שרשרת',
                'created_at': '2025-07-10 15:45:00'
            }
        ],
        'pending_approval': [
            {
                'id': 3,
                'bike': 'Giant Anthem',
                'bike__customer__name': 'דני גרין',
                'diagnosed_at': '2025-07-10 16:00:00'
            }
        ],
        'partially_approved': [
            {
                'id': 4,
                'bike': 'Cannondale Habit',
                'bike__customer__name': 'מיכל אברהם',
                'approved_count': 3,
                'total_items': 5,
                'get_total_approved_price': 450
            }
        ],
        'in_progress': [
            {
                'id': 5,
                'bike': 'Giant Trance X',
                'bike__customer__name': 'רון המכונאי',
                'assigned_mechanic': {'get_full_name': 'עמית הטכנאי'},
                'progress_percentage': 75,
                'completed_items': {'count': 3},
                'approved_items': {'count': 4},
                'pending_items': {'count': 1},
                'recent_completed': [
                    {
                        'description': 'תיקון בלמים',
                        'completed_at': '2025-07-10 18:00:00'
                    }
                ],
                'mechanic_notes': [
                    {
                        'is_blocked': False,
                        'notes': 'הושלם תיקון מערכת הבלמים'
                    }
                ],
                'recent_updates': [
                    {
                        'message': 'התקדמות טובה',
                        'created_at': '2025-07-10 18:30:00'
                    }
                ]
            }
        ]
    }
    
    return render(request, 'workshop/manager_dashboard.html', context)

# בדיקה מקומית
if __name__ == "__main__":
    print("🚵‍♂️ ENDURO BIKE GARAGE - Demo Dashboard")
    print("דמו נתונים ליצירת תצוגה אקסטרימית!")
    print("הנתונים האלה יוצגו בדשבורד עם העיצוב החדש.")
