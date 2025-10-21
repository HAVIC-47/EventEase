#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Notification

def create_test_data():
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
        print(f"Created test user: {user.username} / testpass123")
    else:
        print(f"Test user already exists: {user.username}")

    # Create test notifications
    notifications = [
        {
            'title': 'Welcome to EventEase! 🎉',
            'message': 'Thank you for joining our platform. Start exploring amazing events and venues!',
            'type': 'booking_confirmation'
        },
        {
            'title': 'New Event Available: Music Festival 🎵',
            'message': 'A spectacular music festival is now available for booking. Don\'t miss out on this amazing experience!',
            'type': 'event_booking'
        },
        {
            'title': 'Venue Booking Update 🏢',
            'message': 'Your venue booking request for "Grand Hall" is currently being reviewed by the venue manager.',
            'type': 'venue_booking'
        }
    ]
    
    for notif_data in notifications:
        # Check if notification already exists
        existing = Notification.objects.filter(
            user=user,
            title=notif_data['title']
        ).exists()
        
        if not existing:
            Notification.objects.create(
                user=user,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['type']
            )
            print(f"Created notification: {notif_data['title']}")
    
    total_unread = Notification.objects.filter(user=user, is_read=False).count()
    print(f"\nTotal unread notifications for {user.username}: {total_unread}")
    print(f"You can login with: {user.username} / testpass123")

if __name__ == '__main__':
    create_test_data()
