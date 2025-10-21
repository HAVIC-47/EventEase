#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notification
from notifications.helpers import create_venue_booking_notification, create_event_notification

def create_comprehensive_test_data():
    print("🚀 Creating Comprehensive Test Data for EventEase Notifications")
    print("=" * 60)
    
    # Create multiple test users
    users_data = [
        {'username': 'event_organizer', 'email': 'organizer@example.com', 'first_name': 'Emma', 'last_name': 'Organizer'},
        {'username': 'venue_manager', 'email': 'manager@example.com', 'first_name': 'Victor', 'last_name': 'Manager'},
        {'username': 'regular_user', 'email': 'user@example.com', 'first_name': 'Rachel', 'last_name': 'User'},
    ]
    
    users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✅ Created user: {user.username}")
        else:
            print(f"✅ User exists: {user.username}")
        users[user_data['username']] = user
    
    # Create diverse notifications for each user
    notifications_data = {
        'event_organizer': [
            {
                'title': '🎉 Event Successfully Created!',
                'message': 'Your event "Summer Music Festival 2024" has been successfully created and is now live for bookings.',
                'notification_type': 'event_booking_confirm'
            },
            {
                'title': '📝 New Event Registration',
                'message': 'Rachel User has registered for your event "Tech Conference 2024". Total registrations: 45',
                'notification_type': 'event_registration'
            },
            {
                'title': '⏰ Event Starting Soon!',
                'message': 'Your event "Art Workshop" is starting in 2 hours. Make sure everything is ready!',
                'notification_type': 'upcoming_event'
            }
        ],
        'venue_manager': [
            {
                'title': '🏢 New Venue Booking Request',
                'message': 'Emma Organizer has requested to book "Grand Conference Hall" for March 15, 2024. Please review and respond.',
                'notification_type': 'venue_booking_request'
            },
            {
                'title': '✅ Booking Confirmed',
                'message': 'You have successfully confirmed the venue booking for "Main Auditorium" on April 10, 2024.',
                'notification_type': 'venue_booking_status'
            },
            {
                'title': '❌ Booking Declined',
                'message': 'You have declined the booking request for "Conference Room A" due to maintenance schedule.',
                'notification_type': 'venue_booking_status'
            }
        ],
        'regular_user': [
            {
                'title': '🎫 Event Registration Confirmed',
                'message': 'You have successfully registered for "Digital Marketing Summit 2024". Check your email for the ticket.',
                'notification_type': 'event_registration'
            },
            {
                'title': '📅 Upcoming Event Reminder',
                'message': 'Don\'t forget! "Photography Workshop" is tomorrow at 10:00 AM. Location: Downtown Studio.',
                'notification_type': 'upcoming_event'
            },
            {
                'title': '✅ Venue Booking Approved',
                'message': 'Great news! Your venue booking for "Community Center" on May 20, 2024 has been approved.',
                'notification_type': 'venue_booking_status'
            },
            {
                'title': '🎉 Welcome to EventEase!',
                'message': 'Welcome to our platform! Start exploring amazing events and venues in your area.',
                'notification_type': 'system'
            }
        ]
    }
    
    # Create notifications for each user
    for username, user_notifications in notifications_data.items():
        user = users[username]
        print(f"\n🔸 Creating notifications for {user.first_name} {user.last_name} ({username})")
        
        for notif_data in user_notifications:
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
                print(f"  ✅ {notif_data['title']}")
            else:
                print(f"  ⏭️  Exists: {notif_data['title']}")
    
    # Test helper functions
    print(f"\n🔸 Testing helper functions...")
    try:
        # Test venue booking helper
        venue_notif = create_venue_booking_notification(
            user=users['regular_user'],
            venue_name="Grand Hotel Ballroom",
            booking_date="2024-06-15",
            status="confirmed"
        )
        print(f"  ✅ Venue helper: {venue_notif.title}")
    except Exception as e:
        print(f"  ❌ Venue helper error: {e}")
    
    try:
        # Test event notification helper
        event_notif = create_event_notification(
            user=users['event_organizer'],
            event_name="Innovation Summit 2024",
            event_date="2024-07-01",
            notification_type="event_booking_confirm"
        )
        print(f"  ✅ Event helper: {event_notif.title}")
    except Exception as e:
        print(f"  ❌ Event helper error: {e}")
    
    # Create some read notifications to show the difference
    print(f"\n🔸 Marking some notifications as read...")
    recent_notifications = Notification.objects.all().order_by('-created_at')[:3]
    for notif in recent_notifications:
        notif.mark_as_read()
        print(f"  📖 Marked as read: {notif.title}")
    
    # Display summary statistics
    print(f"\n📊 NOTIFICATION SUMMARY")
    print("=" * 40)
    
    for username, user in users.items():
        total = Notification.objects.filter(user=user).count()
        unread = Notification.objects.filter(user=user, is_read=False).count()
        print(f"{user.first_name} {user.last_name} ({username}):")
        print(f"  📧 Total: {total} | 🔔 Unread: {unread}")
    
    # Display notification types
    print(f"\n📋 NOTIFICATION TYPES COUNT")
    print("=" * 40)
    for notif_type, type_name in Notification.NOTIFICATION_TYPES:
        count = Notification.objects.filter(notification_type=notif_type).count()
        if count > 0:
            print(f"{type_name}: {count}")
    
    print(f"\n🎉 TEST DATA CREATION COMPLETED!")
    print("=" * 60)
    print("🌐 Django server is running at: http://127.0.0.1:8000/")
    print("🔔 View notifications at: http://127.0.0.1:8000/notifications/")
    print("🔑 Login credentials for testing:")
    for username in users.keys():
        print(f"   • {username} / testpass123")
    print("=" * 60)

if __name__ == '__main__':
    create_comprehensive_test_data()
