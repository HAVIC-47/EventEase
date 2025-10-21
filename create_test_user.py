#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Notification

def setup_test_data():
    """Create test user and notifications"""
    try:
        # Create or get test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_active': True
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"✅ Created user: {user.username}")
        else:
            print(f"✅ Using existing user: {user.username}")
        
        # Create test notifications
        notifications_data = [
            {
                'title': 'Welcome to EventEase! 🎉',
                'message': 'Thank you for joining our platform. Start exploring amazing events and venues in your area!',
                'notification_type': 'booking_confirmation'
            },
            {
                'title': 'New Event Available: Music Festival 🎵',
                'message': 'A spectacular summer music festival is now available for booking. Don\'t miss this amazing experience!',
                'notification_type': 'event_booking'
            },
            {
                'title': 'Venue Booking Update 🏢',
                'message': 'Your venue booking request for "Grand Conference Hall" is currently being reviewed by the venue manager.',
                'notification_type': 'venue_booking'
            },
            {
                'title': 'Event Reminder 📅',
                'message': 'Your upcoming event "Tech Conference 2025" starts tomorrow at 9:00 AM. Don\'t forget to attend!',
                'notification_type': 'event_reminder'
            }
        ]
        
        created_count = 0
        for notif_data in notifications_data:
            notification, created = Notification.objects.get_or_create(
                user=user,
                title=notif_data['title'],
                defaults={
                    'message': notif_data['message'],
                    'notification_type': notif_data['notification_type']
                }
            )
            if created:
                created_count += 1
                print(f"✅ Created notification: {notification.title}")
        
        total_notifications = Notification.objects.filter(user=user).count()
        unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
        
        print(f"\n📊 Summary:")
        print(f"   - Created {created_count} new notifications")
        print(f"   - Total notifications for {user.username}: {total_notifications}")
        print(f"   - Unread notifications: {unread_notifications}")
        print(f"\n🔐 Login credentials: {user.username} / testpass123")
        print(f"🌐 Visit: http://127.0.0.1:8000/users/login/")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    setup_test_data()
