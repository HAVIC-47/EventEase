#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Notification

def main():
    # Create or get admin user
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_superuser': True,
            'is_staff': True,
            'first_name': 'Admin',
            'last_name': 'User'
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"Created admin user: {admin.username} / admin123")
    else:
        print(f"Admin user already exists: {admin.username}")

    # Create test notifications
    notifications_created = 0
    test_notifications = [
        {
            'title': 'Welcome to EventEase!',
            'message': 'Thank you for joining our platform. Start exploring events and venues.',
            'type': 'booking_confirmation'
        },
        {
            'title': 'New Event: Music Festival',
            'message': 'A new music festival is available for booking. Check it out!',
            'type': 'event_booking'
        },
        {
            'title': 'Venue Booking Update',
            'message': 'Your venue booking request is being reviewed.',
            'type': 'venue_booking'
        }
    ]
    
    for notif_data in test_notifications:
        # Check if notification already exists
        existing = Notification.objects.filter(
            user=admin,
            title=notif_data['title']
        ).exists()
        
        if not existing:
            Notification.objects.create(
                user=admin,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['type']
            )
            notifications_created += 1
            print(f"Created notification: {notif_data['title']}")
    
    total_unread = Notification.objects.filter(user=admin, is_read=False).count()
    print(f"\nCreated {notifications_created} new notifications")
    print(f"Total unread notifications for {admin.username}: {total_unread}")

if __name__ == '__main__':
    main()
