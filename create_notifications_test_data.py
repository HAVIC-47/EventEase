#!/usr/bin/env python
"""
Create test data for notifications
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Notification

def create_test_data():
    print("Creating test data...")
    
    # Create test users
    users = []
    
    # Create admin user
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
    users.append(admin_user)
    
    # Create regular test user
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
    users.append(test_user)
    
    # Create sample notifications for test user
    sample_notifications = [
        {
            'title': 'Welcome to EventEase!',
            'message': 'Thank you for joining EventEase. Start exploring amazing events near you.',
            'notification_type': 'system',
            'is_read': False,
        },
        {
            'title': 'New Event Available',
            'message': 'A new music concert has been added to your area. Check it out!',
            'notification_type': 'event_registration',
            'is_read': False,
        },
        {
            'title': 'Event Reminder',
            'message': 'Don\'t forget! Your booked event "Tech Conference 2025" is tomorrow.',
            'notification_type': 'event_reminder',
            'is_read': False,
        },
        {
            'title': 'Booking Confirmed',
            'message': 'Your booking for "Art Exhibition" has been confirmed. Booking ID: #12345',
            'notification_type': 'booking_confirmation',
            'is_read': True,
        },
        {
            'title': 'Payment Successful',
            'message': 'Your payment of $50.00 for "Cooking Workshop" has been processed successfully.',
            'notification_type': 'payment_success',
            'is_read': True,
        }
    ]
    
    # Create notifications for test user
    for notif_data in sample_notifications:
        notification, created = Notification.objects.get_or_create(
            user=test_user,
            title=notif_data['title'],
            defaults=notif_data
        )
        if created:
            print(f"✅ Created notification: {notif_data['title']}")
    
    # Create some notifications for admin user
    admin_notifications = [
        {
            'title': 'System Update Complete',
            'message': 'EventEase system has been updated to version 2.1. Check the changelog for new features.',
            'notification_type': 'system',
            'is_read': False,
        },
        {
            'title': 'New User Registration',
            'message': 'A new user has registered on the platform.',
            'notification_type': 'system',
            'is_read': False,
        }
    ]
    
    for notif_data in admin_notifications:
        notification, created = Notification.objects.get_or_create(
            user=admin_user,
            title=notif_data['title'],
            defaults=notif_data
        )
        if created:
            print(f"✅ Created admin notification: {notif_data['title']}")
    
    print("\n🎉 Test data creation completed!")
    print("\nLogin credentials:")
    print("👤 Admin: admin / admin123")
    print("👤 Test User: testuser / testpass123")
    print("\nYou can now:")
    print("1. Login with either account")
    print("2. Check notifications at /core/notifications/")
    print("3. See notification count in the header bell icon")

if __name__ == "__main__":
    create_test_data()
