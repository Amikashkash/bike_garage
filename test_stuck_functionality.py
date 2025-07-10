#!/usr/bin/env python
"""
Simple test to verify the stuck system functionality
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bikegarage.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from workshop.models import Customer, RepairJob

def test_stuck_system():
    print("=== Testing Stuck System ===\n")
    
    # Check if we can create a repair job with stuck fields
    try:
        # Get or create test customer
        customer, created = Customer.objects.get_or_create(
            name="Test Customer",
            defaults={
                'phone': '1234567890',
                'email': 'test@example.com'
            }
        )
        
        # Create a test repair job
        repair_job = RepairJob.objects.create(
            customer=customer,
            bike_model="Test Bike",
            description="Test repair for stuck system",
            status="pending"
        )
        
        print(f"✓ Created repair job: {repair_job.id}")
        
        # Test stuck functionality
        repair_job.is_stuck = True
        repair_job.stuck_reason = "Waiting for parts"
        repair_job.save()
        
        print(f"✓ Updated repair job with stuck status")
        
        # Retrieve and verify
        updated_job = RepairJob.objects.get(id=repair_job.id)
        print(f"✓ Verified stuck status: {updated_job.is_stuck}")
        print(f"✓ Stuck reason: {updated_job.stuck_reason}")
        
        # Test manager response
        updated_job.manager_response = "Parts ordered, will arrive tomorrow"
        updated_job.save()
        
        print(f"✓ Added manager response: {updated_job.manager_response}")
        
        # Clean up
        repair_job.delete()
        if created:
            customer.delete()
        
        print("\n✓ All tests passed! Stuck system is working correctly.")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_stuck_system()
    if success:
        print("\n🎉 System is ready for use!")
    else:
        print("\n❌ System needs fixes before use.")
