#!/usr/bin/env python
import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Notification

def create_test_notifications():
    """Create test notifications for existing users"""
    
    # Get the first user (or create one if none exists)
    try:
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            print(f"Created test user: {user.username}")
        
        print(f"Creating notifications for user: {user.username}")
        
        # Create some test notifications
        notifications = [
            {
                'title': 'Event Registration Confirmed',
                'message': 'Your registration for "Tech Conference 2025" has been confirmed.',
                'notification_type': 'booking_confirmation'
            },
            {
                'title': 'New Event Available',
                'message': 'A new exciting event "Music Festival" is now available for booking.',
                'notification_type': 'event_booking'
            },
            {
                'title': 'Venue Booking Update',
                'message': 'Your venue booking request for "Grand Hall" is under review.',
                'notification_type': 'venue_booking'
            },
            {
                'title': 'Event Reminder',
                'message': 'Don\'t forget! Your event "Workshop Series" starts tomorrow.',
                'notification_type': 'event_reminder'
            },
            {
                'title': 'Payment Confirmation',
                'message': 'Payment of $150 has been received for your event booking.',
                'notification_type': 'booking_confirmation'
            }
        ]
        
        for notif_data in notifications:
            notification = Notification.objects.create(
                user=user,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['notification_type']
            )
            print(f"Created notification: {notification.title}")
        
        unread_count = Notification.objects.filter(user=user, is_read=False).count()
        print(f"\nTotal unread notifications for {user.username}: {unread_count}")
        
    except Exception as e:
        print(f"Error creating notifications: {e}")

if __name__ == '__main__':
    create_test_notifications()
