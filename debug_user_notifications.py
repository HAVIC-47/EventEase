#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from notifications.models import Notification
from django.contrib.auth.models import User

print("=== DEBUG: User Notifications ===")
print(f"Total notifications in database: {Notification.objects.count()}")
print()

# Show all users with notifications
users_with_notifications = User.objects.filter(user_notifications__isnull=False).distinct()
print(f"Users with notifications: {users_with_notifications.count()}")
for user in users_with_notifications:
    count = user.user_notifications.count()
    print(f"  - {user.username}: {count} notifications")

print("\n=== Recent Venue Booking Notifications ===")
venue_notifications = Notification.objects.filter(
    notification_type='venue_booking_status'
).order_by('-created_at')[:10]

for notif in venue_notifications:
    print(f"User: {notif.user.username} | Message: {notif.message} | Read: {notif.is_read} | Created: {notif.created_at}")

print("\n=== All Notification Types ===")
types = Notification.objects.values_list('notification_type', flat=True).distinct()
for ntype in types:
    count = Notification.objects.filter(notification_type=ntype).count()
    print(f"  - {ntype}: {count} notifications")

print("\n=== Test: Create a simple notification ===")
try:
    # Get or create a test user
    test_user, created = User.objects.get_or_create(
        username='debug_test_user',
        defaults={'email': 'debug@test.com'}
    )
    if created:
        print(f"Created test user: {test_user.username}")
    
    # Create a test notification
    test_notification = Notification.objects.create(
        user=test_user,
        message="DEBUG: Test notification to verify system works",
        notification_type='system'
    )
    print(f"✅ Created test notification: {test_notification.id}")
    
    # Verify it exists
    user_notifications = test_user.user_notifications.all()
    print(f"Test user now has {user_notifications.count()} notifications")
    
except Exception as e:
    print(f"❌ Error creating test notification: {e}")

print(f"\n=== Final Count: {Notification.objects.count()} total notifications ===")
