#!/usr/bin/env python
"""
Test SSL Commerz credentials and connection
"""

import os
import sys
import django
import requests

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.conf import settings

def test_ssl_credentials():
    """Test SSL Commerz credentials"""
    print("Testing SSL Commerz Configuration...")
    print(f"Store ID: {settings.SSLCOMMERZ_STORE_ID}")
    print(f"Sandbox Mode: {settings.SSLCOMMERZ_IS_SANDBOX}")
    print(f"Init URL: {settings.SSLCOMMERZ_INIT_URL}")
    
    # Test basic payment initialization
    test_data = {
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
        'total_amount': '100.00',
        'currency': 'BDT',
        'tran_id': 'TEST_' + str(int(time.time())),
        'success_url': 'http://localhost:8000/success/',
        'fail_url': 'http://localhost:8000/fail/',
        'cancel_url': 'http://localhost:8000/cancel/',
        'product_name': 'Test Product',
        'product_category': 'Test',
        'product_profile': 'general',
        'cus_name': 'Test Customer',
        'cus_email': 'test@example.com',
        'cus_add1': 'Test Address',
        'cus_city': 'Dhaka',
        'cus_state': 'Dhaka',
        'cus_postcode': '1000',
        'cus_country': 'Bangladesh',
        'cus_phone': '01700000000',
        'ship_name': 'Test Customer',
        'ship_add1': 'Test Address',
        'ship_city': 'Dhaka',
        'ship_state': 'Dhaka',
        'ship_postcode': '1000',
        'ship_country': 'Bangladesh',
        'shipping_method': 'NO',
    }
    
    try:
        print("\nMaking test request to SSL Commerz...")
        response = requests.post(settings.SSLCOMMERZ_INIT_URL, data=test_data, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"SSL Response Status: {response_data.get('status')}")
            print(f"SSL Response Message: {response_data.get('failedreason', 'Success')}")
            
            if response_data.get('status') == 'SUCCESS':
                print("✅ SSL Commerz credentials are working!")
                print(f"Gateway URL: {response_data.get('GatewayPageURL')}")
            else:
                print("❌ SSL Commerz returned an error:")
                print(f"Error: {response_data.get('failedreason', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")

if __name__ == "__main__":
    import time
    test_ssl_credentials()