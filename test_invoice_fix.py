#!/usr/bin/env python
"""
Test script to verify the invoice generation fix
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.models import Event, EventBooking
from django.contrib.auth.models import User

def test_invoice_generation():
    print("Testing invoice generation fix...")
    
    # Get a test user and event booking
    try:
        # Find an existing user and event booking
        booking = EventBooking.objects.select_related('event', 'user').first()
        
        if not booking:
            print("❌ No event bookings found. Please create a test booking first.")
            return False
        
        print(f"✅ Found test booking: {booking.id}")
        print(f"   Event: {booking.event.title}")
        print(f"   User: {booking.user.username}")
        print(f"   Event ticket_price: ${booking.event.ticket_price}")
        print(f"   Attendees: {booking.attendees_count}")
        print(f"   Total amount: ${booking.total_amount}")
        
        # Test the invoice generation by simulating the view
        client = Client()
        
        # Login as the booking user
        client.force_login(booking.user)
        
        # Try to download the invoice
        response = client.get(f'/auth/download-event-invoice/{booking.id}/')
        
        if response.status_code == 200:
            if response['Content-Type'] == 'application/pdf':
                print("✅ Invoice generation successful!")
                print(f"   Content-Type: {response['Content-Type']}")
                print(f"   Content-Disposition: {response.get('Content-Disposition', 'Not set')}")
                return True
            else:
                print(f"❌ Wrong content type: {response['Content-Type']}")
                return False
        elif response.status_code == 302:
            print(f"❌ Redirected (status 302). Check if there are error messages.")
            return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"   Response content: {response.content[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_invoice_generation()
    if success:
        print("\n🎉 Invoice generation test passed!")
    else:
        print("\n💥 Invoice generation test failed!")