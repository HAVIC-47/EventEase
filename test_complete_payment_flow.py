#!/usr/bin/env python
"""
Test the complete payment flow with intermediate forms
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

def test_complete_payment_flow():
    """Test the complete payment flow with forms"""
    
    # Get test user and booking
    try:
        user = User.objects.get(username='testpayment')
        booking = EventBooking.objects.get(id=59)
        print(f"Testing complete payment flow for booking {booking.id}")
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
    
    # Test main payment page
    print("\n1. Testing main payment page...")
    payment_url = f'/payments/process/{booking.id}/'
    response = client.get(payment_url)
    print(f"Payment page status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Main payment page loaded")
        
        # Test selecting bKash from main payment form
        print("\n2. Testing bKash selection from main form...")
        bkash_selection_response = client.post(payment_url, {
            'payment_method': 'bkash'
        })
        print(f"bKash selection status: {bkash_selection_response.status_code}")
        
        if bkash_selection_response.status_code == 302:
            redirect_url = bkash_selection_response.get('Location', '')
            print(f"✅ Redirected to: {redirect_url}")
            
            if '/payments/bkash/' in redirect_url:
                print("✅ Correctly redirected to bKash form")
                
                # Test bKash form page
                print("\n3. Testing bKash form page...")
                bkash_form_response = client.get(f'/payments/bkash/{booking.id}/')
                print(f"bKash form status: {bkash_form_response.status_code}")
                
                if bkash_form_response.status_code == 200:
                    print("✅ bKash form loaded successfully")
                    
                    # Test bKash form submission
                    print("\n4. Testing bKash form submission...")
                    bkash_submit_response = client.post(f'/payments/bkash/process/{booking.id}/', {
                        'mobile': '1700000000',
                        'pin': '12345',
                        'bkash_method': 'wallet'
                    })
                    print(f"bKash submit status: {bkash_submit_response.status_code}")
                    
                    if bkash_submit_response.status_code == 302:
                        ssl_redirect = bkash_submit_response.get('Location', '')
                        print(f"✅ Final redirect to SSL: {ssl_redirect}")
                        
                        if 'sslcommerz.com' in ssl_redirect:
                            print("✅ Successfully redirected to SSL Commerz gateway!")
                        else:
                            print("❌ Not redirected to SSL Commerz")
                    else:
                        print(f"❌ bKash form submission failed")
                        content = bkash_submit_response.content.decode()[:500]
                        print(f"Content: {content}")
                        
    # Test Nagad flow
    print("\n5. Testing Nagad selection...")
    nagad_selection_response = client.post(payment_url, {
        'payment_method': 'nagad'
    })
    print(f"Nagad selection status: {nagad_selection_response.status_code}")
    
    if nagad_selection_response.status_code == 302:
        redirect_url = nagad_selection_response.get('Location', '')
        print(f"✅ Redirected to: {redirect_url}")
        
        if '/payments/nagad/' in redirect_url:
            print("✅ Correctly redirected to Nagad form")
            
            # Test Nagad form page
            print("\n6. Testing Nagad form page...")
            nagad_form_response = client.get(f'/payments/nagad/{booking.id}/')
            print(f"Nagad form status: {nagad_form_response.status_code}")
            
            if nagad_form_response.status_code == 200:
                print("✅ Nagad form loaded successfully")
                
                # Test Nagad form submission
                print("\n7. Testing Nagad form submission...")
                nagad_submit_response = client.post(f'/payments/nagad/process/{booking.id}/', {
                    'mobile': '1700000000',
                    'pin': '123456',
                    'nagad_method': 'account',
                    'terms': '1'
                })
                print(f"Nagad submit status: {nagad_submit_response.status_code}")
                
                if nagad_submit_response.status_code == 302:
                    ssl_redirect = nagad_submit_response.get('Location', '')
                    print(f"✅ Final redirect to SSL: {ssl_redirect}")
                    
                    if 'sslcommerz.com' in ssl_redirect:
                        print("✅ Successfully redirected to SSL Commerz gateway!")
                    else:
                        print("❌ Not redirected to SSL Commerz")

if __name__ == "__main__":
    test_complete_payment_flow()