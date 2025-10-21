#!/usr/bin/env python
"""
Test script to check for existing bookings and create a fresh test
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth import get_user_model
from events.models import Event, EventBooking, TicketCategory, BookingTicketItem

User = get_user_model()

def check_existing_bookings():
    """Check existing bookings and clear if needed"""
    print("=== Checking Existing Bookings ===\n")
    
    user = User.objects.filter(username='testuser').first()
    if not user:
        print("❌ Test user not found")
        return
        
    # Get the event we're testing with
    event = Event.objects.filter(is_active=True, ticket_categories__isnull=False).first()
    if not event:
        print("❌ No active events with ticket categories found")
        return
        
    print(f"🔍 Checking bookings for user: {user.username}")
    print(f"🔍 For event: {event.title}")
    
    # Check existing bookings
    existing_bookings = EventBooking.objects.filter(user=user, event=event)
    print(f"📋 Found {existing_bookings.count()} existing bookings")
    
    for booking in existing_bookings:
        print(f"   - Booking #{booking.id}: {booking.status} (${booking.amount})")
        ticket_items = BookingTicketItem.objects.filter(booking=booking)
        for item in ticket_items:
            print(f"     → {item.ticket_category.name}: {item.quantity} tickets")
    
    # Optionally delete existing bookings for testing
    if existing_bookings.exists():
        response = input("\n❓ Delete existing bookings for testing? (y/n): ")
        if response.lower() == 'y':
            # Delete ticket items first
            for booking in existing_bookings:
                BookingTicketItem.objects.filter(booking=booking).delete()
            existing_bookings.delete()
            print("✅ Existing bookings deleted")
        else:
            print("ℹ️  Keeping existing bookings")

def test_form_validation():
    """Test form validation without using Django test client"""
    print("\n=== Testing Form Validation ===\n")
    
    from events.forms import EventBookingForm
    
    user = User.objects.filter(username='testuser').first()
    event = Event.objects.filter(is_active=True, ticket_categories__isnull=False).first()
    
    if not user or not event:
        print("❌ Missing user or event")
        return
        
    # Test valid form data
    category = event.ticket_categories.first()
    form_data = {
        'attendee_name': 'Test User',
        'attendee_email': 'test@example.com',
        'attendee_phone': '123-456-7890',
        'special_requests': '',
        f'quantity_{category.id}': 1
    }
    
    print(f"📝 Testing form with data: {form_data}")
    
    form = EventBookingForm(data=form_data, event=event, user=user)
    
    if form.is_valid():
        print("✅ Form is valid")
        selected_tickets = form.get_selected_tickets()
        print(f"✅ Selected tickets: {selected_tickets}")
    else:
        print("❌ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"   - {field}: {errors}")

def create_test_event():
    """Create a simple test event for booking"""
    print("\n=== Creating Test Event ===\n")
    
    from venues.models import Venue
    from django.utils import timezone
    from datetime import timedelta
    
    # Get a venue
    venue = Venue.objects.first()
    if not venue:
        print("❌ No venues found")
        return None
        
    # Create a simple event
    event = Event.objects.create(
        title="Test Booking Event",
        description="A test event for booking functionality",
        event_type="conference",
        venue=venue,
        venue_name=venue.name,
        venue_address=venue.address,
        start_date=timezone.now() + timedelta(days=30),
        end_date=timezone.now() + timedelta(days=30, hours=2),
        max_attendees=100,
        ticket_price=50.00,
        is_free=False,
        is_active=True,
        organizer=User.objects.filter(profile__role='admin').first()
    )
    
    # Create ticket categories
    TicketCategory.objects.create(
        event=event,
        name="General",
        description="General admission ticket",
        price=50.00,
        quantity_available=50
    )
    
    TicketCategory.objects.create(
        event=event,
        name="VIP",
        description="VIP ticket with premium access",
        price=100.00,
        quantity_available=20
    )
    
    print(f"✅ Created test event: {event.title}")
    print(f"✅ Created {event.ticket_categories.count()} ticket categories")
    
    return event

if __name__ == "__main__":
    check_existing_bookings()
    test_form_validation()
    
    # Optionally create a new test event
    create_new = input("\n❓ Create a new test event? (y/n): ")
    if create_new.lower() == 'y':
        create_test_event()
