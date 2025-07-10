#!/usr/bin/env python
"""
Test script to check the current system status
"""
import os
import django
import sqlite3

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

print("=== System Status Check ===\n")

# 1. Check database file exists
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    print(f"✓ Database file exists: {db_path}")
    
    # Check database structure
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if workshop_repairjob table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='workshop_repairjob';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✓ workshop_repairjob table exists")
            
            # Get table structure
            cursor.execute("PRAGMA table_info(workshop_repairjob);")
            columns = cursor.fetchall()
            
            print("\nTable columns:")
            for col in columns:
                print(f"  - {col[1]}: {col[2]}")
            
            # Check for stuck fields specifically
            stuck_fields = ['is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response']
            existing_columns = [col[1] for col in columns]
            
            print("\nStuck fields status:")
            for field in stuck_fields:
                if field in existing_columns:
                    print(f"  ✓ {field} exists")
                else:
                    print(f"  ✗ {field} MISSING")
        else:
            print("✗ workshop_repairjob table does not exist")
        
        conn.close()
    except Exception as e:
        print(f"✗ Database error: {e}")
else:
    print(f"✗ Database file not found: {db_path}")

# 2. Check Django models
try:
    from workshop.models import RepairJob
    fields = [f.name for f in RepairJob._meta.get_fields()]
    print(f"\n✓ RepairJob model loaded successfully")
    print(f"Model fields: {fields}")
    
    # Check if stuck fields are in the model
    stuck_fields = ['is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response']
    print("\nModel stuck fields status:")
    for field in stuck_fields:
        if field in fields:
            print(f"  ✓ {field} in model")
        else:
            print(f"  ✗ {field} NOT in model")
            
except Exception as e:
    print(f"✗ Model loading error: {e}")

# 3. Check migrations
try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM django_migrations WHERE app='workshop' ORDER BY id;")
    migrations = cursor.fetchall()
    
    print(f"\n✓ Applied migrations:")
    for migration in migrations:
        print(f"  - {migration[1]}: {migration[2]}")
        
except Exception as e:
    print(f"✗ Migration check error: {e}")

print("\n=== End Status Check ===")
