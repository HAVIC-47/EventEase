#!/usr/bin/env python
"""
Test script to check booking and payment functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth import get_user_model
from events.models import Event, EventBooking, TicketCategory, BookingTicketItem
from django.test import Client
from django.urls import reverse

User = get_user_model()

def test_booking_functionality():
    """Test the booking process"""
    print("=== Testing Booking Functionality ===\n")
    
    try:
        # Get a test user and event
        user = User.objects.filter(username='testuser').first()
        if not user:
            print("❌ Test user not found. Please run test_notification_bell.py first.")
            return
            
        # Get an active event with ticket categories
        event = Event.objects.filter(is_active=True, ticket_categories__isnull=False).first()
        if not event:
            print("❌ No active events with ticket categories found.")
            return
            
        print(f"✅ Testing with user: {user.username}")
        print(f"✅ Testing with event: {event.title}")
        print(f"✅ Event has {event.ticket_categories.count()} ticket categories")
        
        # Check ticket categories
        for category in event.ticket_categories.all():
            print(f"   - {category.name}: ${category.price} ({category.tickets_available} available)")
        
        # Test the booking URL
        client = Client()
        client.force_login(user)
        
        # Get the booking page
        booking_url = reverse('events:event_book', kwargs={'pk': event.pk})
        print(f"\n📍 Testing booking URL: {booking_url}")
        
        response = client.get(booking_url)
        print(f"✅ GET request status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Error accessing booking page: {response.status_code}")
            return
            
        # Test POST request with sample data
        category = event.ticket_categories.first()
        post_data = {
            'attendee_name': 'Test User',
            'attendee_email': 'test@example.com',
            'attendee_phone': '123-456-7890',
            'special_requests': 'No special requests',
            f'quantity_{category.id}': 1
        }
        
        print(f"\n📝 Testing POST with data: {post_data}")
        
        response = client.post(booking_url, post_data)
        print(f"✅ POST request status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"✅ Redirect (probably successful): {response.url}")
        elif response.status_code == 200:
            # Check for form errors
            if hasattr(response, 'context') and 'form' in response.context:
                form = response.context['form']
                if form.errors:
                    print(f"❌ Form errors: {form.errors}")
                else:
                    print("✅ Form submitted without errors")
            
        # Check if booking was created
        booking = EventBooking.objects.filter(user=user, event=event).first()
        if booking:
            print(f"✅ Booking created: #{booking.id}")
            print(f"   Status: {booking.status}")
            print(f"   Payment Status: {booking.payment_status}")
            print(f"   Amount: ${booking.amount}")
            
            # Check ticket items
            ticket_items = BookingTicketItem.objects.filter(booking=booking)
            print(f"   Ticket items: {ticket_items.count()}")
            for item in ticket_items:
                print(f"     - {item.ticket_category.name}: {item.quantity} × ${item.price_per_ticket}")
        else:
            print("❌ No booking was created")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

def check_database_integrity():
    """Check if database tables and relationships are working"""
    print("\n=== Checking Database Integrity ===\n")
    
    try:
        # Check models
        events_count = Event.objects.count()
        bookings_count = EventBooking.objects.count()
        categories_count = TicketCategory.objects.count()
        ticket_items_count = BookingTicketItem.objects.count()
        
        print(f"✅ Events: {events_count}")
        print(f"✅ Bookings: {bookings_count}")
        print(f"✅ Ticket Categories: {categories_count}")
        print(f"✅ Booking Ticket Items: {ticket_items_count}")
        
        # Check for events with categories
        events_with_categories = Event.objects.filter(ticket_categories__isnull=False).distinct().count()
        print(f"✅ Events with ticket categories: {events_with_categories}")
        
        # Check recent bookings
        recent_bookings = EventBooking.objects.order_by('-booking_date')[:5]
        print(f"\n📋 Recent bookings:")
        for booking in recent_bookings:
            print(f"   - #{booking.id}: {booking.user.username} → {booking.event.title} (${booking.amount})")
            
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database_integrity()
    test_booking_functionality()
