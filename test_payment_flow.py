#!/usr/bin/env python
"""
Test payment flow programmatically
"""

import os
import sys
import django
import requests
from urllib.parse import urljoin

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from events.models import EventBooking

def test_payment_flow():
    """Test the payment flow"""
    
    # Get test user and booking
    try:
        user = User.objects.get(username='testpayment')
        booking = EventBooking.objects.get(id=59)
        print(f"Testing payment for booking {booking.id}")
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
    
    # Access bKash payment page
    print("\nTesting bKash payment page...")
    bkash_url = f'/payments/bkash/{booking.id}/'
    response = client.get(bkash_url)
    print(f"bKash page status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ bKash payment page loaded successfully")
    else:
        print(f"❌ bKash payment page failed: {response.status_code}")
        print(f"Content: {response.content.decode()[:500]}")
        return
    
    # Submit bKash payment form
    print("\nTesting bKash payment processing...")
    bkash_process_url = f'/payments/bkash/process/{booking.id}/'
    payment_data = {
        'mobile': '1700000000',
        'pin': '12345',
        'bkash_method': 'wallet'
    }
    
    response = client.post(bkash_process_url, payment_data)
    print(f"bKash processing status: {response.status_code}")
    
    if response.status_code == 302:  # Redirect expected
        print(f"✅ Redirect to: {response.get('Location', 'Unknown')}")
    else:
        print(f"❌ Payment processing failed: {response.status_code}")
        print(f"Content: {response.content.decode()[:1000]}")

if __name__ == "__main__":
    test_payment_flow()