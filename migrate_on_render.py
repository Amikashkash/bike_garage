#!/usr/bin/env python
"""
Script to run migrations on Render server
Run this script in the Render shell or add it to your deploy commands
"""
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
    django.setup()
    
    print("Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("Migration completed successfully!")
