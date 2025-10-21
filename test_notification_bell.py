#!/usr/bin/env python
"""
Test script to create notifications and test the red notification bell functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()

def create_test_notifications():
    """Create test notifications for testing the bell functionality"""
    try:
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'testuser@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"Created test user: {user.username}")
        else:
            print(f"Using existing user: {user.username}")
        
        # Create some test notifications
        notifications = [
            {
                'notification_type': 'event_booking_confirm',
                'title': 'Booking Confirmed',
                'message': 'Your booking for "Tech Conference 2025" has been confirmed.',
            },
            {
                'notification_type': 'upcoming_event',
                'title': 'Event Reminder',
                'message': 'Your event "Tech Conference 2025" is starting in 1 hour.',
            },
            {
                'notification_type': 'system',
                'title': 'Payment Received',
                'message': 'Payment of $150.00 has been received for your booking.',
            }
        ]
        
        created_notifications = []
        for notif_data in notifications:
            notification = Notification.objects.create(
                user=user,
                notification_type=notif_data['notification_type'],
                title=notif_data['title'],
                message=notif_data['message'],
                is_read=False  # Make sure they're unread
            )
            created_notifications.append(notification)
            print(f"Created notification: {notification.title}")
        
        print(f"\nCreated {len(created_notifications)} unread notifications for user: {user.username}")
        print(f"Total unread notifications for user: {user.user_notifications.filter(is_read=False).count()}")
        
        return user, created_notifications
        
    except Exception as e:
        print(f"Error creating test notifications: {e}")
        return None, []

def check_user_notifications():
    """Check existing notifications for all users"""
    try:
        users = User.objects.all()
        print("\n=== Current Notification Status ===")
        
        for user in users:
            total_notifications = user.user_notifications.count()
            unread_notifications = user.user_notifications.filter(is_read=False).count()
            read_notifications = user.user_notifications.filter(is_read=True).count()
            
            print(f"\nUser: {user.username}")
            print(f"  Total notifications: {total_notifications}")
            print(f"  Unread notifications: {unread_notifications}")
            print(f"  Read notifications: {read_notifications}")
            
            if unread_notifications > 0:
                print(f"  Recent unread notifications:")
                for notif in user.user_notifications.filter(is_read=False)[:3]:
                    print(f"    - {notif.title}")
                    
    except Exception as e:
        print(f"Error checking notifications: {e}")

def mark_notifications_as_read(username):
    """Mark all notifications as read for a specific user"""
    try:
        user = User.objects.get(username=username)
        unread_count = user.user_notifications.filter(is_read=False).count()
        
        if unread_count > 0:
            user.user_notifications.filter(is_read=False).update(is_read=True)
            print(f"Marked {unread_count} notifications as read for user: {username}")
        else:
            print(f"No unread notifications found for user: {username}")
            
    except User.DoesNotExist:
        print(f"User '{username}' not found")
    except Exception as e:
        print(f"Error marking notifications as read: {e}")

if __name__ == "__main__":
    print("=== Notification Bell Test Script ===")
    print("\n1. Checking current notification status...")
    check_user_notifications()
    
    print("\n2. Creating test notifications...")
    user, notifications = create_test_notifications()
    
    if user:
        print("\n3. Updated notification status...")
        check_user_notifications()
        
        print(f"\n=== Test Instructions ===")
        print(f"1. Open your browser and go to: http://127.0.0.1:8000/")
        print(f"2. Login with username: {user.username}, password: testpass123")
        print(f"3. Check if the notification bell is RED (indicating {len(notifications)} unread notifications)")
        print(f"4. Click on notifications to view them")
        print(f"5. The bell should turn back to GREEN when all notifications are read")
        print(f"\nTo mark all notifications as read, run:")
        print(f"python test_notification_bell.py mark_read {user.username}")
    
    # Handle command line arguments
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "mark_read" and len(sys.argv) > 2:
            mark_notifications_as_read(sys.argv[2])
            check_user_notifications()
        elif sys.argv[1] == "check":
            check_user_notifications()
