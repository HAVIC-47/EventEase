#!/usr/bin/env python
"""
Test script to debug multi-category event booking button issue
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

def test_multi_category_booking_forms():
    """Test multi-category booking with different approaches"""
    print("\n=== Testing Multi-Category Booking Forms ===")
    
    # Get event 9
    event = Event.objects.get(id=9)
    print(f"Event: {event.title}")
    
    categories = list(event.ticket_categories.all())
    for cat in categories:
        print(f"  Category {cat.id}: {cat.name} - ${cat.price}")
    
    # Get test user
    User = get_user_model()
    test_user, created = User.objects.get_or_create(
        username='testuser_button',
        defaults={
            'email': 'button@test.com',
            'first_name': 'Button',
            'last_name': 'Test'
        }
    )
    
    client = Client()
    client.force_login(test_user)
    
    print("\n--- Test 1: Direct Booking Form (No Pre-selection) ---")
    response = client.get(reverse('events:event_book', args=[event.id]))
    print(f"GET response status: {response.status_code}")
    print(f"Response context keys: {list(response.context.keys()) if response.context else 'No context'}")
    if response.context:
        print(f"has_categories: {response.context.get('has_categories')}")
        print(f"is_checkout: {response.context.get('is_checkout')}")
    
    # Try to submit form with category selection
    booking_data = {
        'attendee_name': 'Button Test',
        'attendee_email': 'button@test.com',
        'attendee_phone': '1234567890',
        'quantity_5': 1,  # Select 1 General ticket
        'quantity_6': 0,  # No VIP tickets
    }
    
    print(f"\nPOST data: {booking_data}")
    response = client.post(reverse('events:event_book', args=[event.id]), booking_data)
    print(f"POST response status: {response.status_code}")
    print(f"Response URL: {response.url if hasattr(response, 'url') else 'No redirect'}")
    
    # Check if booking was created
    booking = EventBooking.objects.filter(event=event, user=test_user).last()
    if booking:
        print(f"✅ Booking created: ID {booking.id}, Amount: ${booking.amount}")
    else:
        print("❌ No booking created")
    
    print("\n--- Test 2: Checkout Flow (Pre-selected) ---")
    # Test checkout flow with pre-selected tickets
    checkout_url = reverse('events:event_book', args=[event.id]) + '?quantity_5=2&quantity_6=1'
    print(f"Checkout URL: {checkout_url}")
    
    response = client.get(checkout_url)
    print(f"GET checkout response status: {response.status_code}")
    if response.context:
        print(f"is_checkout: {response.context.get('is_checkout')}")
        print(f"total_amount: {response.context.get('total_amount')}")
        print(f"total_tickets: {response.context.get('total_tickets')}")
    
    # Submit checkout form
    checkout_data = {
        'attendee_name': 'Button Test Checkout',
        'attendee_email': 'button@test.com',
        'attendee_phone': '1234567890',
        'quantity_5': 2,  # From URL params
        'quantity_6': 1,  # From URL params
    }
    
    response = client.post(checkout_url, checkout_data)
    print(f"POST checkout response status: {response.status_code}")
    print(f"Response URL: {response.url if hasattr(response, 'url') else 'No redirect'}")
    
    # Check latest booking
    booking = EventBooking.objects.filter(event=event, user=test_user).last()
    if booking:
        print(f"✅ Checkout booking created: ID {booking.id}, Amount: ${booking.amount}")
        print(f"   Ticket items: {booking.ticket_items.count()}")
        for item in booking.ticket_items.all():
            print(f"     {item.ticket_category.name}: {item.quantity} x ${item.price_per_ticket}")
    else:
        print("❌ No checkout booking created")

if __name__ == '__main__':
    test_multi_category_booking_forms()
