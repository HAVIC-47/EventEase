#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notification
from notifications.helpers import create_venue_booking_notification, create_event_notification

def test_notification_system():
    print("🧪 Testing Notification System...")
    print("=" * 50)
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Test user already exists: {user.username}")

    # Test 1: Create notifications using the model directly
    print("\n🔹 Test 1: Creating notifications directly...")
    
    test_notifications = [
        {
            'title': 'Welcome to EventEase! 🎉',
            'message': 'Thank you for joining our platform. Start exploring amazing events and venues!',
            'notification_type': 'system'
        },
        {
            'title': 'Event Booking Confirmed ✅',
            'message': 'Your booking for "Summer Music Festival" has been confirmed. Get ready for an amazing experience!',
            'notification_type': 'event_booking_confirm'
        },
        {
            'title': 'Venue Booking Status Update 🏢',
            'message': 'Your venue booking request for "Grand Hall" has been approved by the venue manager.',
            'notification_type': 'venue_booking_status'
        },
        {
            'title': 'Upcoming Event Reminder ⏰',
            'message': 'Don\'t forget! Your event "Tech Conference 2024" is starting tomorrow at 9:00 AM.',
            'notification_type': 'upcoming_event'
        },
        {
            'title': 'New Venue Booking Request 📋',
            'message': 'You have received a new booking request for your venue "Conference Center".',
            'notification_type': 'venue_booking_request'
        },
        {
            'title': 'Event Registration Success 🎫',
            'message': 'You have successfully registered for "Art Exhibition 2024". Check your email for details.',
            'notification_type': 'event_registration'
        }
    ]
    
    for notif_data in test_notifications:
        # Check if notification already exists
        existing = Notification.objects.filter(
            user=user,
            title=notif_data['title']
        ).exists()
        
        if not existing:
            notification = Notification.objects.create(
                user=user,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['notification_type']
            )
            print(f"  ✅ Created: {notif_data['title']}")
        else:
            print(f"  ⏭️  Exists: {notif_data['title']}")

    # Test 2: Test helper functions
    print("\n🔹 Test 2: Testing helper functions...")
    
    try:
        # Test venue booking notification
        venue_notif = create_venue_booking_notification(
            user=user,
            venue_name="Test Venue",
            booking_date="2024-02-15",
            status="confirmed"
        )
        print(f"  ✅ Venue helper: {venue_notif.title}")
    except Exception as e:
        print(f"  ❌ Venue helper error: {e}")
    
    try:
        # Test event notification
        event_notif = create_event_notification(
            user=user,
            event_name="Test Event",
            event_date="2024-03-01",
            notification_type="event_booking_confirm"
        )
        print(f"  ✅ Event helper: {event_notif.title}")
    except Exception as e:
        print(f"  ❌ Event helper error: {e}")

    # Test 3: Check notification counts and types
    print("\n🔹 Test 3: Notification statistics...")
    
    total_notifications = Notification.objects.filter(user=user).count()
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
    
    print(f"  📊 Total notifications: {total_notifications}")
    print(f"  📊 Unread notifications: {unread_notifications}")
    
    # Count by type
    for notif_type, type_name in Notification.NOTIFICATION_TYPES:
        count = Notification.objects.filter(user=user, notification_type=notif_type).count()
        if count > 0:
            print(f"  📊 {type_name}: {count}")

    # Test 4: Display recent notifications
    print("\n🔹 Test 4: Recent notifications...")
    recent_notifications = Notification.objects.filter(user=user).order_by('-created_at')[:5]
    
    for notif in recent_notifications:
        status = "📧 Unread" if not notif.is_read else "✅ Read"
        print(f"  {status} [{notif.notification_type}] {notif.title}")

    print(f"\n🎉 Test completed! Login credentials: {user.username} / testpass123")
    print("🌐 Run the Django server and visit /notifications/ to see the notifications page")

if __name__ == '__main__':
    test_notification_system()
