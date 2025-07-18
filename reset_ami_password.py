#!/usr/bin/env python
"""
Reset or create ami superuser
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')
django.setup()

from django.contrib.auth.models import User
from workshop.models import UserProfile

def reset_ami_password():
    print("🔑 Resetting AMI Superuser Password")
    print("=" * 40)
    
    # Clean up any orphaned profiles first
    orphaned_profiles = UserProfile.objects.filter(user__isnull=True)
    if orphaned_profiles.exists():
        count = orphaned_profiles.count()
        orphaned_profiles.delete()
        print(f"🧹 Cleaned up {count} orphaned profiles")
    
    # Check if ami user exists
    ami_user = User.objects.filter(username='ami').first()
    
    if ami_user:
        print(f"✅ Found existing user: ami")
        print(f"   Is superuser: {ami_user.is_superuser}")
        print(f"   Is staff: {ami_user.is_staff}")
        
        # Reset password
        ami_user.set_password('ami123')
        ami_user.save()
        print("✅ Password reset to: ami123")
        
        # Ensure it's a superuser
        if not ami_user.is_superuser:
            ami_user.is_superuser = True
            ami_user.is_staff = True
            ami_user.save()
            print("✅ Updated to superuser status")
        
        # Check/create profile
        profile, created = UserProfile.objects.get_or_create(
            user=ami_user,
            defaults={'role': 'manager'}
        )
        if created:
            print("✅ Created manager profile")
        else:
            print(f"✅ Existing profile role: {profile.role}")
            
    else:
        print("❌ User 'ami' not found. Creating new superuser...")
        
        try:
            # Create new superuser
            ami_user = User.objects.create_superuser(
                username='ami',
                email='ami@bikegarage.com',
                password='ami123',
                first_name='Ami',
                last_name='Manager'
            )
            
            # Create profile
            profile, created = UserProfile.objects.get_or_create(
                user=ami_user,
                defaults={'role': 'manager'}
            )
            
            print("✅ Created new superuser 'ami'")
            print("✅ Password set to: ami123")
            print("✅ Created manager profile")
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            # Try to clean up if user was created but profile failed
            try:
                User.objects.filter(username='ami').delete()
                print("🧹 Cleaned up partial user creation")
            except:
                pass
            return
    
    print("\n🎯 AMI Superuser Credentials:")
    print("   Username: ami")
    print("   Password: ami123")
    print("   Role: Manager + Superuser")
    print("   Can access: /admin/ and manager dashboard")

if __name__ == "__main__":
    reset_ami_password()
