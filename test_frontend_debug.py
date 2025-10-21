#!/usr/bin/env python
"""
Simple frontend test to verify multi-category booking works
"""

import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.models import Event

def test_frontend_booking():
    """Test that the booking form renders correctly with quantity inputs"""
    
    event = Event.objects.get(id=9)
    print(f"Testing event: {event.title}")
    print(f"Has categories: {event.ticket_categories.exists()}")
    
    User = get_user_model()
    test_user, _ = User.objects.get_or_create(
        username='frontend_test',
        defaults={'email': 'frontend@test.com'}
    )
    
    client = Client()
    client.force_login(test_user)
    
    # Test regular booking form (no pre-selection)
    print("\n--- Regular Booking Form ---")
    response = client.get(f'/events/{event.id}/book/')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for quantity inputs
        quantity_inputs = content.count('name="quantity_')
        print(f"Quantity inputs found: {quantity_inputs}")
        
        # Check for has_categories variable
        if 'hasCategories = true' in content:
            print("✅ hasCategories = true found in template")
        elif 'hasCategories = false' in content:
            print("⚠️  hasCategories = false found in template")
        else:
            print("❌ hasCategories variable not found")
        
        # Check for form
        if 'class="booking-form"' in content:
            print("✅ Booking form found")
        else:
            print("❌ Booking form not found")
            
        # Check for submit button
        if 'type="submit"' in content:
            print("✅ Submit button found")
        else:
            print("❌ Submit button not found")
    
    # Test checkout form (with pre-selection)
    print("\n--- Checkout Form (Pre-selected) ---")
    response = client.get(f'/events/{event.id}/book/?quantity_5=1')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for hidden inputs
        hidden_inputs = content.count('type="hidden" name="quantity_')
        print(f"Hidden quantity inputs found: {hidden_inputs}")
        
        # Check for checkout flag
        if 'is_checkout: true' in content:
            print("✅ is_checkout = true found")
        elif 'is_checkout: false' in content:
            print("⚠️  is_checkout = false found")
        else:
            print("❌ is_checkout variable not found")

if __name__ == '__main__':
    test_frontend_booking()
