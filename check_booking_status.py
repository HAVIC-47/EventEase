#!/usr/bin/env python
"""
Simple test to check if event booking is working
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from events.models import Event, EventBooking

def test_booking():
    print("🧪 Testing Event Booking")
    
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username='booking_test', 
        defaults={'email': 'booking@test.com', 'first_name': 'Test', 'last_name': 'User'}
    )
    
    client = Client()
    client.force_login(user)
    
    # Test 1: Multi-category event
    print("\n1. Testing Multi-category Event (ID: 9)")
    try:
        event = Event.objects.get(id=9)
        print(f"   Event: {event.title}")
        
        response = client.get(f'/events/{event.id}/book/')
        print(f"   GET request: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Booking form loads successfully")
            
            # Try to submit booking
            booking_data = {
                'attendee_name': 'Test User',
                'attendee_email': 'booking@test.com',
                'attendee_phone': '1234567890',
                'quantity_5': 1,  # General ticket
                'quantity_6': 0,  # No VIP tickets
            }
            
            response = client.post(f'/events/{event.id}/book/', booking_data)
            print(f"   POST request: {response.status_code}")
            
            if response.status_code == 302:
                print("   ✅ Booking submitted successfully (redirected)")
                
                # Check if booking was created
                booking = EventBooking.objects.filter(event=event, user=user).last()
                if booking:
                    print(f"   ✅ Booking created: ID {booking.id}, Amount: ${booking.amount}")
                else:
                    print("   ❌ No booking record found")
            else:
                print(f"   ❌ Booking submission failed")
        else:
            print(f"   ❌ Booking form failed to load")
            
    except Event.DoesNotExist:
        print("   ❌ Event 9 does not exist")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Legacy event (no categories)
    print("\n2. Testing Legacy Event (ID: 11)")
    try:
        event = Event.objects.get(id=11)
        print(f"   Event: {event.title}")
        
        response = client.get(f'/events/{event.id}/book/')
        print(f"   GET request: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Booking form loads successfully")
            
            # Try to submit booking
            booking_data = {
                'attendee_name': 'Test User',
                'attendee_email': 'booking@test.com',
                'attendee_phone': '1234567890',
            }
            
            response = client.post(f'/events/{event.id}/book/', booking_data)
            print(f"   POST request: {response.status_code}")
            
            if response.status_code == 302:
                print("   ✅ Booking submitted successfully (redirected)")
                
                # Check if booking was created
                booking = EventBooking.objects.filter(event=event, user=user).last()
                if booking:
                    print(f"   ✅ Booking created: ID {booking.id}, Amount: ${booking.amount}")
                else:
                    print("   ❌ No booking record found")
            else:
                print(f"   ❌ Booking submission failed")
        else:
            print(f"   ❌ Booking form failed to load")
            
    except Event.DoesNotExist:
        print("   ❌ Event 11 does not exist")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*50)
    print("Summary: Event booking system status")

if __name__ == '__main__':
    test_booking()
