#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
בדיקה פשוטה לפני push
"""

import subprocess
import sys
import os

def simple_check():
    """בדיקה פשוטה לפני push"""
    print("=== בדיקה לפני Push ===")
    
    # בדיקת שינויים
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        print("יש שינויים לpush")
    else:
        print("אין שינויים")
        return True
    
    # בדיקת Django
    try:
        result = subprocess.run(["python", "manage.py", "check"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Django check: OK")
        else:
            print("Django check: FAILED")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Django check error: {e}")
        return False
    
    # בדיקת migrations
    try:
        result = subprocess.run(["python", "manage.py", "makemigrations", "--dry-run"], 
                              capture_output=True, text=True, timeout=30)
        if "No changes detected" in result.stdout:
            print("Migrations: OK")
        else:
            print("יש migrations חדשים - הרץ makemigrations")
    except Exception as e:
        print(f"Migrations check error: {e}")
    
    print("=== בדיקה הושלמה ===")
    print("אם הכל בסדר, הרץ:")
    print("git add .")
    print("git commit -m 'תיאור השינוי'")
    print("git push origin main")
    
    return True

if __name__ == "__main__":
    success = simple_check()
    sys.exit(0 if success else 1)
