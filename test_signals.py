#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta, timezone
from decimal import Decimal

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from venues.models import Venue, VenueBooking
from events.models import Event, EventBooking
from notifications.models import Notification

def test_automatic_notifications():
    print("🧪 Testing Automatic Notification Signals")
    print("=" * 50)
    
    # Create test users
    organizer, _ = User.objects.get_or_create(
        username='event_organizer',
        defaults={'email': 'organizer@test.com', 'first_name': 'Event', 'last_name': 'Organizer'}
    )
    
    customer, _ = User.objects.get_or_create(
        username='customer',
        defaults={'email': 'customer@test.com', 'first_name': 'John', 'last_name': 'Customer'}
    )
    
    venue_manager, _ = User.objects.get_or_create(
        username='venue_manager',
        defaults={'email': 'manager@test.com', 'first_name': 'Venue', 'last_name': 'Manager'}
    )
    
    print(f"✅ Test users ready")
    
    # Create a test venue
    venue, _ = Venue.objects.get_or_create(
        name='Test Conference Hall',
        defaults={
            'description': 'A beautiful conference hall for events',
            'venue_type': 'conference_hall',
            'manager': venue_manager,
            'address': '123 Event Street',
            'city': 'Event City',
            'state': 'Event State',
            'zipcode': '12345',
            'country': 'USA',
            'capacity': 200,
            'hourly_rate': Decimal('150.00'),
            'amenities': 'WiFi, Projector, Sound System',
            'is_available': True
        }
    )
    print(f"✅ Test venue ready: {venue.name}")
    
    # Create a test event
    start_date = datetime.now(timezone.utc) + timedelta(days=7)
    end_date = start_date + timedelta(hours=3)
    
    event, _ = Event.objects.get_or_create(
        title='Test Tech Conference',
        defaults={
            'description': 'An amazing tech conference',
            'organizer': organizer,
            'venue': venue,
            'start_date': start_date,
            'end_date': end_date,
            'max_attendees': 100,
            'ticket_price': Decimal('50.00'),
            'category': 'technology',
            'is_active': True
        }
    )
    print(f"✅ Test event ready: {event.title}")
    
    # Count initial notifications
    initial_count = Notification.objects.count()
    print(f"📊 Initial notifications count: {initial_count}")
    
    print(f"\n🔹 Test 1: Creating Venue Booking...")
    
    # Test 1: Create a venue booking (should trigger venue_booking_status_notification)
    venue_booking = VenueBooking.objects.create(
        venue=venue,
        user=customer,
        event_title='Customer Conference',
        event_description='A customer-organized conference',
        start_date=datetime.now(timezone.utc) + timedelta(days=10),
        end_date=datetime.now(timezone.utc) + timedelta(days=10, hours=4),
        total_amount=Decimal('600.00'),
        contact_email=customer.email,
        contact_phone='555-0123',
        status='pending'
    )
    print(f"✅ Created venue booking: {venue_booking}")
    
    # Test 2: Update venue booking status (should trigger notification)
    print(f"\n🔹 Test 2: Updating Venue Booking Status...")
    venue_booking.status = 'confirmed'
    venue_booking.save()
    print(f"✅ Updated venue booking status to: {venue_booking.status}")
    
    # Test 3: Create an event booking (should trigger event_booking_notification)
    print(f"\n🔹 Test 3: Creating Event Booking...")
    event_booking = EventBooking.objects.create(
        event=event,
        user=customer,
        status='pending',
        attendees_count=2,
        total_amount=Decimal('100.00')
    )
    print(f"✅ Created event booking: {event_booking}")
    
    # Test 4: Update event booking status
    print(f"\n🔹 Test 4: Updating Event Booking Status...")
    event_booking.status = 'confirmed'
    event_booking.save()
    print(f"✅ Updated event booking status to: {event_booking.status}")
    
    # Check for new notifications
    final_count = Notification.objects.count()
    new_notifications = final_count - initial_count
    print(f"\n📊 Final notifications count: {final_count}")
    print(f"📊 New notifications created: {new_notifications}")
    
    # Display recent notifications
    print(f"\n🔔 Recent Notifications:")
    recent_notifications = Notification.objects.all().order_by('-created_at')[:10]
    
    for i, notif in enumerate(recent_notifications, 1):
        status = "📧 Unread" if not notif.is_read else "✅ Read"
        print(f"  {i}. {status} [{notif.notification_type}] {notif.user.username}")
        print(f"     {notif.title}")
        print(f"     {notif.message[:100]}...")
        print()
    
    # Test upcoming event notifications
    print(f"🔹 Test 5: Testing Upcoming Event Notifications...")
    
    # Create an event that's starting soon
    upcoming_start = datetime.now(timezone.utc) + timedelta(hours=2)
    upcoming_end = upcoming_start + timedelta(hours=2)
    
    upcoming_event, _ = Event.objects.get_or_create(
        title='Upcoming Workshop',
        defaults={
            'description': 'A workshop starting soon',
            'organizer': organizer,
            'venue': venue,
            'start_date': upcoming_start,
            'end_date': upcoming_end,
            'max_attendees': 50,
            'ticket_price': Decimal('25.00'),
            'category': 'workshop',
            'is_active': True
        }
    )
    
    # Create a booking for the upcoming event
    upcoming_booking = EventBooking.objects.create(
        event=upcoming_event,
        user=customer,
        status='confirmed',
        attendees_count=1,
        total_amount=Decimal('25.00')
    )
    print(f"✅ Created upcoming event booking: {upcoming_booking}")
    
    # Run the upcoming notifications command
    from notifications.signals import send_upcoming_event_notifications
    try:
        send_upcoming_event_notifications()
        print(f"✅ Upcoming event notifications sent")
    except Exception as e:
        print(f"❌ Error sending upcoming notifications: {e}")
    
    # Final count
    very_final_count = Notification.objects.count()
    print(f"\n📊 Very final notifications count: {very_final_count}")
    print(f"📊 Total new notifications: {very_final_count - initial_count}")
    
    print(f"\n🎉 Automatic notification testing completed!")
    print("=" * 50)
    print("🌐 View notifications at: http://127.0.0.1:8000/notifications/")
    print("🔑 Login as:")
    print(f"   • customer / testpass123 (should have booking notifications)")
    print(f"   • venue_manager / testpass123 (should have venue notifications)")
    print(f"   • event_organizer / testpass123 (should have event notifications)")

if __name__ == '__main__':
    test_automatic_notifications()
