#!/usr/bin/env python
"""
Test direct SSL payment flow
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from events.models import EventBooking

def test_direct_ssl_payment():
    """Test the direct SSL payment flow"""
    
    # Get test user and booking
    try:
        user = User.objects.get(username='testpayment')
        booking = EventBooking.objects.get(id=59)
        print(f"Testing direct SSL payment for booking {booking.id}")
    except (User.DoesNotExist, EventBooking.DoesNotExist):
        print("Test user or booking not found. Run create_payment_test_booking.py first")
        return
    
    # Create test client
    client = Client()
    
    # Login as test user
    login_success = client.login(username='testpayment', password='testpass123')
    if not login_success:
        print("❌ Login failed")
        return
    print("✅ Login successful")
    
    # Test bKash direct payment
    print("\nTesting bKash direct SSL payment...")
    bkash_url = f'/payments/bkash/{booking.id}/'
    response = client.get(bkash_url, follow=True)
    
    print(f"Final response status: {response.status_code}")
    print(f"Redirect chain: {[r.url for r in response.redirect_chain]}")
    
    if response.status_code == 200:
        # Check if we're on SSL Commerz page
        if 'sslcommerz.com' in response.request.get('HTTP_HOST', ''):
            print("✅ Successfully redirected to SSL Commerz bKash payment page")
        else:
            print("✅ Page loaded - checking content for SSL indicators")
            content = response.content.decode()
            if 'bkash' in content.lower() or 'ssl' in content.lower():
                print("✅ SSL Commerz payment content detected")
            else:
                print("Content preview:", content[:200])
    
    # Test Nagad direct payment
    print("\nTesting Nagad direct SSL payment...")
    nagad_url = f'/payments/nagad/{booking.id}/'
    response = client.get(nagad_url, follow=True)
    
    print(f"Final response status: {response.status_code}")
    print(f"Redirect chain: {[r.url for r in response.redirect_chain]}")
    
    if response.status_code == 200:
        # Check if we're on SSL Commerz page
        if 'sslcommerz.com' in response.request.get('HTTP_HOST', ''):
            print("✅ Successfully redirected to SSL Commerz Nagad payment page")
        else:
            print("✅ Page loaded - checking content for SSL indicators")
            content = response.content.decode()
            if 'nagad' in content.lower() or 'ssl' in content.lower():
                print("✅ SSL Commerz payment content detected")
            else:
                print("Content preview:", content[:200])

if __name__ == "__main__":
    test_direct_ssl_payment()