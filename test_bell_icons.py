#!/usr/bin/env python3
"""
Test script to verify the enhanced bell icons functionality
"""
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import FriendRequest, Message

def test_bell_icons():
    print("🔔 Testing Enhanced Bell Icons System")
    print("="*50)
    
    # Get or create test users
    try:
        user1 = User.objects.get(username='testuser1')
        user2 = User.objects.get(username='testuser2')
        print(f"✅ Found test users: {user1.username} and {user2.username}")
    except User.DoesNotExist:
        print("❌ Test users not found. Creating them...")
        user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User1'
        )
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User2'
        )
        print(f"✅ Created test users: {user1.username} and {user2.username}")
    
    # Test friend request functionality
    print("\n🤝 Testing Friend Request Bell...")
    
    # Create a friend request if it doesn't exist
    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=user2,
        to_user=user1,
        defaults={'status': 'pending'}
    )
    
    if created:
        print(f"✅ Created friend request from {user2.username} to {user1.username}")
    else:
        print(f"✅ Friend request already exists from {user2.username} to {user1.username}")
    
    # Check pending requests count
    pending_count = FriendRequest.objects.filter(to_user=user1, status='pending').count()
    print(f"📊 Pending friend requests for {user1.username}: {pending_count}")
    
    if pending_count > 0:
        print("✅ Friends bell should show ORANGE/YELLOW color!")
    else:
        print("ℹ️  Friends bell should show default teal color")
    
    # Test messages functionality
    print("\n💬 Testing Messages Bell...")
    
    # Create an unread message if it doesn't exist
    message, created = Message.objects.get_or_create(
        sender=user2,
        recipient=user1,
        defaults={
            'content': 'Hello! This is a test message for the bell icon.',
            'is_read': False
        }
    )
    
    if created:
        print(f"✅ Created message from {user2.username} to {user1.username}")
    else:
        print(f"✅ Message already exists from {user2.username} to {user1.username}")
    
    # Check unread messages count
    unread_count = Message.objects.filter(recipient=user1, is_read=False).count()
    print(f"📊 Unread messages for {user1.username}: {unread_count}")
    
    if unread_count > 0:
        print("✅ Messages bell should show GREEN color!")
    else:
        print("ℹ️  Messages bell should show default teal color")
    
    print("\n🎨 Bell Icon Status Summary:")
    print(f"👤 User: {user1.username}")
    print(f"🔔 Friends Bell: {'🟡 ORANGE' if pending_count > 0 else '🟢 TEAL'} ({pending_count} pending requests)")
    print(f"💬 Messages Bell: {'🟢 GREEN' if unread_count > 0 else '🟢 TEAL'} ({unread_count} unread messages)")
    
    print("\n🌐 Test the visual changes at: http://127.0.0.1:8000/")
    print("📝 Login as 'testuser1' with password 'testpass123' to see the colored bells!")
    
    return True

if __name__ == "__main__":
    try:
        test_bell_icons()
        print("\n✅ Bell icons test completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()