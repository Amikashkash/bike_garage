#!/usr/bin/env python
"""
Quick setup to ensure demo users exist and system is ready
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile, Customer, RepairJob

def setup_demo_users():
    print("🔧 Setting up demo users...")
    
    # Create mechanic user
    mechanic_user, created = User.objects.get_or_create(
        username='mechanic',
        defaults={
            'first_name': 'יוסי',
            'last_name': 'המכונאי',
            'email': 'mechanic@bikegarage.co.il'
        }
    )
    if created:
        mechanic_user.set_password('123456')
        mechanic_user.save()
    
    # Create mechanic profile
    mechanic_profile, created = UserProfile.objects.get_or_create(
        user=mechanic_user,
        defaults={'role': 'mechanic'}
    )
    
    # Create manager user
    manager_user, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'first_name': 'שרה',
            'last_name': 'המנהלת',
            'email': 'manager@bikegarage.co.il'
        }
    )
    if created:
        manager_user.set_password('123456')
        manager_user.save()
    
    # Create manager profile
    manager_profile, created = UserProfile.objects.get_or_create(
        user=manager_user,
        defaults={'role': 'manager'}
    )
    
    print("✅ Demo users ready:")
    print(f"   Mechanic: {mechanic_user.username} (password: 123456)")
    print(f"   Manager:  {manager_user.username} (password: 123456)")
    
    return mechanic_user, manager_user

def create_demo_repair():
    print("\n🚴 Creating demo repair job...")
    
    # Get or create demo customer
    customer, created = Customer.objects.get_or_create(
        name="דני כהן",
        defaults={
            'phone': '050-1234567',
            'email': 'danny@example.com'
        }
    )
    
    # Get mechanic
    mechanic = User.objects.get(username='mechanic')
    
    # Create demo repair
    repair, created = RepairJob.objects.get_or_create(
        customer=customer,
        bike_model="Trek Mountain Bike",
        defaults={
            'description': 'בעיה בהילוכים וצריך להחליף שרשרת',
            'status': 'in_progress',
            'assigned_mechanic': mechanic
        }
    )
    
    if created:
        print(f"✅ Demo repair created: {repair.id}")
    else:
        print(f"ℹ️  Demo repair already exists: {repair.id}")
    
    return repair

if __name__ == "__main__":
    print("🚀 BikeGarage Demo Setup")
    print("="*40)
    
    try:
        mechanic, manager = setup_demo_users()
        repair = create_demo_repair()
        
        print("\n🎉 Setup completed successfully!")
        print("\nTo test the system:")
        print("1. Go to http://127.0.0.1:8000/login/")
        print("2. Login as 'mechanic' / '123456' for mechanic interface")
        print("3. Login as 'manager' / '123456' for manager interface")
        print("4. Test the stuck/working buttons on the repair job")
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()
