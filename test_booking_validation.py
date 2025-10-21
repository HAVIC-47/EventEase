#!/usr/bin/env python
"""
Test script to validate that booking works for both:
1. Legacy events (no categories)  
2. Multi-category events
"""

import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.models import Event, EventBooking, TicketCategory
from django.urls import reverse

def test_legacy_event_booking():
    """Test booking an event without categories"""
    print("\n=== Testing Legacy Event Booking (No Categories) ===")
    
    # Get a legacy event
    legacy_event = Event.objects.filter(is_active=True).exclude(
        id__in=[event.id for event in Event.objects.all() if event.ticket_categories.exists()]
    ).first()
    
    if not legacy_event:
        print("❌ No legacy events found!")
        return False
    
    print(f"Testing event: {legacy_event.title} (ID: {legacy_event.id})")
    print(f"Has categories: {legacy_event.ticket_categories.exists()}")
    
    # Get or create a test user
    User = get_user_model()
    test_user, created = User.objects.get_or_create(
        username='testuser_legacy',
        defaults={
            'email': 'legacy@test.com',
            'first_name': 'Legacy',
            'last_name': 'User'
        }
    )
    
    # Create a client and login
    client = Client()
    client.force_login(test_user)
    
    # Test GET request to booking form
    response = client.get(reverse('events:event_book', args=[legacy_event.id]))
    print(f"GET booking form status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Booking form loaded successfully")
        # Check if has_categories is in context
        if hasattr(response, 'context') and response.context:
            print(f"has_categories in context: {response.context.get('has_categories', 'Not found')}")
        else:
            print("Context not available in response")
    else:
        print(f"❌ Failed to load booking form")
        return False
    
    # Test POST request to create booking
    booking_data = {
        'attendee_name': f"{test_user.first_name} {test_user.last_name}",
        'attendee_email': test_user.email,
        'attendee_phone': '1234567890',
    }
    
    response = client.post(reverse('events:event_book', args=[legacy_event.id]), booking_data)
    print(f"POST booking status: {response.status_code}")
    
    # Check if booking was created
    booking = EventBooking.objects.filter(event=legacy_event, user=test_user).first()
    if booking:
        print(f"✅ Booking created successfully: {booking.id}")
        print(f"   Amount: ${booking.amount}")
        print(f"   Status: {booking.status}")
        return True
    else:
        print(f"❌ Booking was not created")
        print(f"   Response status: {response.status_code}")
        if response.status_code == 200:
            # Form had errors - but context might not be available in test
            print("   Form may have had errors (check manually)")
        return False

def test_multi_category_event_booking():
    """Test booking an event with multiple categories"""
    print("\n=== Testing Multi-Category Event Booking ===")
    
    # Get a multi-category event
    multi_event = None
    for event in Event.objects.filter(is_active=True):
        if event.ticket_categories.count() > 1:
            multi_event = event
            break
    
    if not multi_event:
        print("❌ No multi-category events found!")
        return False
    
    print(f"Testing event: {multi_event.title} (ID: {multi_event.id})")
    print(f"Has categories: {multi_event.ticket_categories.exists()}")
    print(f"Category count: {multi_event.ticket_categories.count()}")
    
    categories = list(multi_event.ticket_categories.all())
    for cat in categories:
        print(f"  - {cat.name}: ${cat.price}")
    
    # Get or create a test user
    User = get_user_model()
    test_user, created = User.objects.get_or_create(
        username='testuser_multi',
        defaults={
            'email': 'multi@test.com',
            'first_name': 'Multi',
            'last_name': 'User'
        }
    )
    
    # Create a client and login
    client = Client()
    client.force_login(test_user)
    
    # Test GET request to booking form
    response = client.get(reverse('events:event_book', args=[multi_event.id]))
    print(f"GET booking form status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ Booking form loaded successfully")
        if hasattr(response, 'context') and response.context:
            print(f"has_categories in context: {response.context.get('has_categories', 'Not found')}")
        else:
            print("Context not available in response")
    else:
        print(f"❌ Failed to load booking form")
        return False
    
    # Test POST request with ticket selection
    booking_data = {
        'attendee_name': f"{test_user.first_name} {test_user.last_name}",
        'attendee_email': test_user.email,
        'attendee_phone': '1234567890',
    }
    
    # Add quantities for categories (select 1 ticket from first category)
    first_category = categories[0]
    booking_data[f'quantity_{first_category.id}'] = 1
    
    print(f"Booking with 1 ticket from '{first_category.name}' category")
    
    response = client.post(reverse('events:event_book', args=[multi_event.id]), booking_data)
    print(f"POST booking status: {response.status_code}")
    
    # Check if booking was created
    booking = EventBooking.objects.filter(event=multi_event, user=test_user).first()
    if booking:
        print(f"✅ Booking created successfully: {booking.id}")
        print(f"   Amount: ${booking.amount}")
        print(f"   Status: {booking.status}")
        print(f"   Attendees: {booking.attendees_count}")
        
        # Check ticket items
        ticket_items = booking.ticket_items.all()
        print(f"   Ticket items: {ticket_items.count()}")
        for item in ticket_items:
            print(f"     - {item.ticket_category.name}: {item.quantity} x ${item.price_per_ticket}")
        return True
    else:
        print(f"❌ Booking was not created")
        print(f"   Response status: {response.status_code}")
        if response.status_code == 200:
            # Form had errors
            print("   Form may have had errors (check manually)")
        return False

def main():
    print("🧪 Testing Event Booking Validation Fix")
    
    # Test both scenarios
    legacy_success = test_legacy_event_booking()
    multi_success = test_multi_category_event_booking()
    
    print(f"\n=== Results ===")
    print(f"Legacy Event Booking: {'✅ PASS' if legacy_success else '❌ FAIL'}")
    print(f"Multi-Category Event Booking: {'✅ PASS' if multi_success else '❌ FAIL'}")
    
    if legacy_success and multi_success:
        print(f"\n🎉 All tests passed! Both legacy and multi-category events can be booked.")
    else:
        print(f"\n⚠️  Some tests failed. Check the output above for details.")

if __name__ == '__main__':
    main()
