#!/usr/bin/env python3
"""
Test script to verify the enhanced header icon notification system.
This script will create test notifications, friend requests, and messages
to verify that all three icons (notifications, friends, messages) work correctly.
"""

import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notification
from users.models import FriendRequest, Message
from django.utils import timezone
from datetime import timedelta

def test_notification_system():
    """Test the complete notification system with all three icon types."""
    print("🔔 Testing Enhanced Header Icon Notification System")
    print("=" * 55)
    
    # Get or create test users
    try:
        user1 = User.objects.get(username='testuser')
        print(f"✅ Found test user: {user1.username}")
    except User.DoesNotExist:
        user1 = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created test user: {user1.username}")
    
    try:
        user2 = User.objects.get(username='frienduser')
        print(f"✅ Found friend user: {user2.username}")
    except User.DoesNotExist:
        user2 = User.objects.create_user(
            username='frienduser',
            email='friend@example.com',
            password='testpass123',
            first_name='Friend',
            last_name='User'
        )
        print(f"✅ Created friend user: {user2.username}")
    
    print("\n🎯 Testing Notification Bell (Regular Notifications)")
    print("-" * 50)
    
    # Create test notifications
    notification_count = Notification.objects.filter(user=user1, is_read=False).count()
    print(f"📊 Current unread notifications: {notification_count}")
    
    if notification_count == 0:
        # Create test notification
        Notification.objects.create(
            user=user1,
            title='Test Notification',
            message='Test notification for header icon',
            notification_type='system',
            is_read=False
        )
        print("✅ Created test notification - NOTIFICATION BELL should turn RED")
    else:
        print("✅ Unread notifications exist - NOTIFICATION BELL should be RED")
    
    print("\n👥 Testing Friends Bell (Friend Requests)")
    print("-" * 45)
    
    # Create test friend request
    friend_request_count = FriendRequest.objects.filter(to_user=user1, status='pending').count()
    print(f"📊 Current pending friend requests: {friend_request_count}")
    
    if friend_request_count == 0:
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=user2,
            to_user=user1,
            defaults={'status': 'pending', 'created_at': timezone.now()}
        )
        if created:
            print("✅ Created test friend request - FRIENDS BELL should turn RED")
        else:
            print("✅ Friend request already exists - FRIENDS BELL should be RED")
    else:
        print("✅ Pending friend requests exist - FRIENDS BELL should be RED")
    
    print("\n💬 Testing Messages Bell (Unread Messages)")
    print("-" * 48)
    
    # Create test message
    unread_message_count = Message.objects.filter(receiver=user1, is_read=False).count()
    print(f"📊 Current unread messages: {unread_message_count}")
    
    if unread_message_count == 0:
        Message.objects.create(
            sender=user2,
            receiver=user1,
            content='Test message for header icon notification',
            is_read=False
        )
        print("✅ Created test message - MESSAGES BELL should turn RED")
    else:
        print("✅ Unread messages exist - MESSAGES BELL should be RED")
    
    print("\n🎨 Visual Testing Summary")
    print("-" * 30)
    print("1. 🔔 NOTIFICATION BELL: Should be RED with breathing animation")
    print("2. 👥 FRIENDS BELL: Should be RED with breathing animation") 
    print("3. 💬 MESSAGES BELL: Should be RED with breathing animation")
    print("4. All three icons should have the same teal color when no notifications")
    print("5. All three icons should turn red when notifications are present")
    print("6. Clicking each icon should mark respective notifications as read")
    
    print("\n🧪 Testing Mark-as-Read Functionality")
    print("-" * 40)
    print("👆 Click each red icon in the browser to test mark-as-read:")
    print("   • Notification bell → Should remove red state")
    print("   • Friends bell → Should remove red state") 
    print("   • Messages bell → Should remove red state")
    
    print("\n✨ All test data created successfully!")
    print("🌐 Visit http://127.0.0.1:8000/ to see the enhanced icons in action")
    
    return True

if __name__ == "__main__":
    test_notification_system()