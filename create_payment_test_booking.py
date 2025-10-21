#!/usr/bin/env python
"""
Create a test booking for payment testing
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking
from venues.models import Venue

def create_test_booking():
    """Create a test booking for payment testing"""
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='testpayment',
        defaults={
            'email': 'testpayment@example.com',
            'first_name': 'Payment',
            'last_name': 'Tester'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing test user: {user.username}")
    
    # Get or create test venue
    venue, created = Venue.objects.get_or_create(
        name='Payment Test Venue',
        defaults={
            'description': 'Test venue for payment testing',
            'venue_type': 'conference_hall',
            'manager': user,
            'address': 'Test Address, Dhaka',
            'city': 'Dhaka',
            'state': 'Dhaka',
            'zipcode': '1000',
            'country': 'Bangladesh',
            'capacity': 100,
            'price_per_hour': 1000.00,
            'contact_email': 'venue@example.com',
            'contact_phone': '01700000000'
        }
    )
    if created:
        print(f"Created test venue: {venue.name}")
    else:
        print(f"Using existing test venue: {venue.name}")
    
    # Get or create test event
    event, created = Event.objects.get_or_create(
        title='Payment Test Event',
        defaults={
            'description': 'Test event for payment testing',
            'venue': venue,
            'venue_name': venue.name,
            'venue_address': venue.address,
            'start_date': datetime.now() + timedelta(days=7),
            'end_date': datetime.now() + timedelta(days=7, hours=3),
            'organizer': user,
            'max_attendees': 50,
            'ticket_price': 500.00,
            'is_active': True
        }
    )
    if created:
        print(f"Created test event: {event.title}")
    else:
        print(f"Using existing test event: {event.title}")
    
    # Create test booking
    booking, created = EventBooking.objects.get_or_create(
        event=event,
        user=user,
        defaults={
            'attendee_name': 'Payment Tester',
            'attendee_email': 'testpayment@example.com',
            'attendee_phone': '01700000000',
            'attendees_count': 1,
            'amount': 500.00,
            'status': 'confirmed'
        }
    )
    
    if created:
        print(f"Created test booking: {booking.id}")
    else:
        print(f"Using existing test booking: {booking.id}")
    
    print(f"\nTest booking details:")
    print(f"Booking ID: {booking.id}")
    print(f"Event: {booking.event.title}")
    print(f"Amount: ৳{booking.amount}")
    print(f"User: {booking.user.username}")
    print(f"Phone: {booking.attendee_phone}")
    
    print(f"\nPayment URL: http://127.0.0.1:8001/payments/process/{booking.id}/")
    print(f"bKash URL: http://127.0.0.1:8001/payments/bkash/{booking.id}/")
    print(f"Nagad URL: http://127.0.0.1:8001/payments/nagad/{booking.id}/")
    
    return booking

if __name__ == "__main__":
    create_test_booking()