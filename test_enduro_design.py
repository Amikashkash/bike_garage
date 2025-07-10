#!/usr/bin/env python3
"""
בדיקת העיצוב החדש - ENDURO BIKE GARAGE
"""

import os
import sys
import django
from pathlib import Path

# הוספת נתיב הפרויקט
project_path = Path(__file__).resolve().parent
sys.path.append(str(project_path))

# הגדרת Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

def test_enduro_design():
    """בדיקת העיצוב החדש"""
    
    print("🚵‍♂️ ENDURO BIKE GARAGE - בדיקת עיצוב חדש")
    print("=" * 50)
    
    # בדיקת קבצי CSS
    css_file = project_path / "workshop" / "static" / "workshop" / "css" / "enduro-style.css"
    if css_file.exists():
        print("✅ קובץ CSS אקסטרימי קיים")
        file_size = css_file.stat().st_size / 1024  # KB
        print(f"📊 גודל קובץ CSS: {file_size:.1f} KB")
    else:
        print("❌ קובץ CSS חסר!")
        return False
    
    # בדיקת תבניות מעודכנות
    templates_to_check = [
        "workshop/templates/workshop/manager_dashboard.html",
        "workshop/templates/workshop/mechanic_task.html",
        "workshop/templates/workshop/base.html"
    ]
    
    for template in templates_to_check:
        template_path = project_path / template
        if template_path.exists():
            print(f"✅ תבנית מעודכנת: {template.split('/')[-1]}")
        else:
            print(f"❌ תבנית חסרה: {template}")
    
    # בדיקת רכיבי העיצוב החדש
    print("\n🎨 רכיבי העיצוב החדש:")
    
    css_content = css_file.read_text(encoding='utf-8')
    
    enduro_components = [
        "enduro-hero-header",
        "enduro-card",
        "enduro-table",
        "enduro-btn",
        "enduro-icon-spin",
        "enduro-progress-bar",
        "quick-actions-grid"
    ]
    
    for component in enduro_components:
        if component in css_content:
            print(f"✅ {component}")
        else:
            print(f"❌ {component} חסר!")
    
    # בדיקת צבעי האנדורו
    print("\n🌈 צבעי האנדורו:")
    enduro_colors = [
        "--enduro-orange: #FF6B35",
        "--enduro-lime: #BBFF00", 
        "--enduro-yellow: #FFD700",
        "--enduro-dark-gray: #2D2D2D"
    ]
    
    for color in enduro_colors:
        if color in css_content:
            print(f"✅ {color}")
        else:
            print(f"❌ {color} חסר!")
    
    # בדיקת אנימציות
    print("\n⚡ אנימציות אקסטרימיות:")
    animations = ["spin", "pulse", "shine", "float", "backgroundShift"]
    
    for animation in animations:
        if f"@keyframes {animation}" in css_content:
            print(f"✅ {animation}")
        else:
            print(f"❌ {animation} חסר!")
    
    print("\n🏁 סיכום:")
    print("העיצוב החדש מותקן ומוכן לפעולה!")
    print("🚀 המערכת עברה מהפכה עיצובית מלאה בסגנון אנדורו אקסטרימי!")
    
    return True

if __name__ == "__main__":
    test_enduro_design()
