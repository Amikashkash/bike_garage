#!/usr/bin/env python
"""
view זמני להרצת תיקון מיגרציות דרך הדפדפן
"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import os

@csrf_exempt
def emergency_migration_fix(request):
    """view חירום לתיקון מיגרציות - להרצה חד פעמית בלבד"""
    
    # בטיחות - רק למשתמש מנהל
    if not request.user.is_authenticated or not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'manager':
        return HttpResponse("אין הרשאה", status=403)
    
    if request.method == 'POST' and request.POST.get('confirm') == 'yes':
        try:
            # הרצת הסקריפט
            result = subprocess.run(['python', 'run_migrations_auto.py'], 
                                  capture_output=True, text=True, timeout=60)
            
            output = f"""
            <h2>תוצאות תיקון מיגרציות</h2>
            <h3>Output:</h3>
            <pre>{result.stdout}</pre>
            <h3>Errors:</h3>
            <pre>{result.stderr}</pre>
            <h3>Return Code: {result.returncode}</h3>
            
            <hr>
            <a href="/manager-dashboard/">חזרה לדשבורד מנהל</a>
            """
            
            return HttpResponse(output)
            
        except Exception as e:
            return HttpResponse(f"שגיאה: {e}")
    
    # טופס אישור
    html = """
    <h2>תיקון חירום למיגרציות</h2>
    <p><strong>אזהרה:</strong> פעולה זו תתקן את מסד הנתונים</p>
    <form method="post">
        <input type="hidden" name="confirm" value="yes">
        <button type="submit" style="background:red;color:white;padding:10px;">
            אשר - הרץ תיקון מיגרציות
        </button>
    </form>
    <br>
    <a href="/manager-dashboard/">ביטול</a>
    """
    
    return HttpResponse(html)
