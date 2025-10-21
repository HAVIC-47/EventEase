#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.views import create_notification

def create_sample_notifications():
    """Create sample notifications for the first user"""
    try:
        # Get first user or create a test user
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
        
        # Create test notifications
        create_notification(
            user=user,
            title="Welcome to EventEase!",
            message="Thank you for joining EventEase. Start exploring events and venues in your area.",
            notification_type='booking_confirmation'
        )
        
        create_notification(
            user=user,
            title="New Event Available: Music Festival 2025",
            message="A new exciting music festival is now available for booking. Don't miss out!",
            notification_type='event_booking'
        )
        
        create_notification(
            user=user,
            title="Venue Booking Reminder",
            message="Your venue booking for Grand Hall is pending approval from the venue manager.",
            notification_type='venue_booking'
        )
        
        create_notification(
            user=user,
            title="Event Reminder",
            message="Your event 'Tech Conference' is starting tomorrow at 9:00 AM. See you there!",
            notification_type='event_reminder'
        )
        
        create_notification(
            user=user,
            title="Payment Confirmation",
            message="Your payment of $150 has been successfully processed for your event booking.",
            notification_type='booking_confirmation'
        )
        
        # Count unread notifications
        from core.models import Notification
        unread_count = Notification.objects.filter(user=user, is_read=False).count()
        print(f"Created 5 test notifications. Total unread: {unread_count}")
        
    except Exception as e:
        print(f"Error creating notifications: {e}")

if __name__ == '__main__':
    create_sample_notifications()
