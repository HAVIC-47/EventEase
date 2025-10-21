#!/usr/bin/env python
"""
Setup script for the new notification system
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notification

def setup_notification_system():
    """Setup the complete notification system"""
    print("🚀 Setting up notification system...")
    
    # Create test users
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@eventease.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: admin / admin123")
    else:
        print(f"✅ Admin user already exists: admin")
    
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@eventease.com',
            'first_name': 'Test',
            'last_name': 'User',
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Created test user: testuser / testpass123")
    else:
        print(f"✅ Test user already exists: testuser")
    
    # Create venue manager
    venue_manager, created = User.objects.get_or_create(
        username='venuemanager',
        defaults={
            'email': 'venue@eventease.com',
            'first_name': 'Venue',
            'last_name': 'Manager',
        }
    )
    if created:
        venue_manager.set_password('venue123')
        venue_manager.save()
        print(f"✅ Created venue manager: venuemanager / venue123")
    else:
        print(f"✅ Venue manager already exists: venuemanager")
    
    # Create event manager
    event_manager, created = User.objects.get_or_create(
        username='eventmanager',
        defaults={
            'email': 'event@eventease.com',
            'first_name': 'Event',
            'last_name': 'Manager',
        }
    )
    if created:
        event_manager.set_password('event123')
        event_manager.save()
        print(f"✅ Created event manager: eventmanager / event123")
    else:
        print(f"✅ Event manager already exists: eventmanager")
    
    # Clear existing notifications
    Notification.objects.all().delete()
    print("✅ Cleared existing notifications")
    
    # Create sample notifications for test user
    sample_notifications = [
        {
            'user': test_user,
            'title': 'Event Booking Confirmed',
            'message': 'Your booking for "Tech Conference 2025" has been confirmed. Booking ID: #EVT001',
            'notification_type': 'event_booking_confirm',
            'is_read': False,
        },
        {
            'user': test_user,
            'title': 'Venue Booking Status Update',
            'message': 'Your venue booking request for "Grand Ballroom" has been approved.',
            'notification_type': 'venue_booking_status',
            'is_read': False,
        },
        {
            'user': test_user,
            'title': 'Upcoming Event Reminder',
            'message': 'Don\'t forget! "Music Festival 2025" is happening tomorrow at 6 PM.',
            'notification_type': 'upcoming_event',
            'is_read': False,
        },
        {
            'user': test_user,
            'title': 'Welcome to EventEase!',
            'message': 'Thank you for joining EventEase. Explore amazing events and venues near you.',
            'notification_type': 'system',
            'is_read': True,
        },
    ]
    
    for notif_data in sample_notifications:
        Notification.objects.create(**notif_data)
    
    print(f"✅ Created {len(sample_notifications)} notifications for test user")
    
    # Create sample notifications for venue manager
    venue_notifications = [
        {
            'user': venue_manager,
            'title': 'New Venue Booking Request',
            'message': 'A new booking request has been received for "Conference Hall A" from John Doe.',
            'notification_type': 'venue_booking_request',
            'is_read': False,
        },
        {
            'user': venue_manager,
            'title': 'Venue Booking Confirmed',
            'message': 'Booking #VEN123 for "Grand Ballroom" has been confirmed and payment received.',
            'notification_type': 'venue_booking_status',
            'is_read': False,
        },
    ]
    
    for notif_data in venue_notifications:
        Notification.objects.create(**notif_data)
    
    print(f"✅ Created {len(venue_notifications)} notifications for venue manager")
    
    # Create sample notifications for event manager
    event_notifications = [
        {
            'user': event_manager,
            'title': 'New Event Registration',
            'message': 'Sarah Johnson has registered for "Tech Conference 2025". Total registrations: 45',
            'notification_type': 'event_registration',
            'is_read': False,
        },
        {
            'user': event_manager,
            'title': 'Event Registration Update',
            'message': 'Mike Wilson has registered for "Music Festival 2025". Total registrations: 120',
            'notification_type': 'event_registration',
            'is_read': False,
        },
    ]
    
    for notif_data in event_notifications:
        Notification.objects.create(**notif_data)
    
    print(f"✅ Created {len(event_notifications)} notifications for event manager")
    
    print("\n🎉 Notification system setup completed!")
    print("\nLogin credentials:")
    print("👤 Test User: testuser / testpass123 (3 unread notifications)")
    print("👤 Venue Manager: venuemanager / venue123 (2 unread notifications)")
    print("👤 Event Manager: eventmanager / event123 (2 unread notifications)")
    print("👤 Admin: admin / admin123")
    print("\nTest URLs:")
    print("🏠 Home: http://127.0.0.1:8000/")
    print("🔐 Login: http://127.0.0.1:8000/auth/login/")
    print("🔔 Notifications: http://127.0.0.1:8000/notifications/")
    print("📊 API Count: http://127.0.0.1:8000/notifications/api/count/")

if __name__ == "__main__":
    setup_notification_system()
