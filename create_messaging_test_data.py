#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile, Friendship, Message

def create_test_messaging_data():
    """Create test users, friendships, and messages for testing"""
    
    print("=== Creating Test Messaging Data ===")
    
    # Create test users
    users_data = [
        {'username': 'alice', 'email': 'alice@test.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
        {'username': 'bob', 'email': 'bob@test.com', 'first_name': 'Bob', 'last_name': 'Smith'},
        {'username': 'charlie', 'email': 'charlie@test.com', 'first_name': 'Charlie', 'last_name': 'Brown'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✅ Created user: {user.username}")
        else:
            print(f"👤 User already exists: {user.username}")
        created_users.append(user)
    
    # Create friendships
    alice, bob, charlie = created_users
    
    friendships_to_create = [
        (alice, bob),
        (alice, charlie),
        (bob, charlie)
    ]
    
    for user1, user2 in friendships_to_create:
        # Create bidirectional friendships
        friendship1, created1 = Friendship.objects.get_or_create(user1=user1, user2=user2)
        friendship2, created2 = Friendship.objects.get_or_create(user1=user2, user2=user1)
        
        if created1 or created2:
            print(f"✅ Created friendship: {user1.username} ↔ {user2.username}")
        else:
            print(f"👥 Friendship already exists: {user1.username} ↔ {user2.username}")
    
    # Create test messages
    messages_to_create = [
        (alice, bob, "Hey Bob! How are you doing?"),
        (bob, alice, "Hi Alice! I'm great, thanks for asking!"),
        (alice, bob, "That's awesome! Want to grab coffee sometime?"),
        (bob, alice, "Absolutely! How about tomorrow at 3 PM?"),
        (alice, charlie, "Charlie! Long time no see!"),
        (charlie, alice, "Alice! Yes, it's been ages! How have you been?"),
        (alice, charlie, "I've been great! Working on some exciting projects."),
        (bob, charlie, "Hey Charlie, did you see the game last night?"),
        (charlie, bob, "Yes! What an amazing match! The final goal was incredible."),
    ]
    
    for sender, receiver, content in messages_to_create:
        message, created = Message.objects.get_or_create(
            sender=sender,
            receiver=receiver,
            content=content,
            defaults={'is_read': False}
        )
        if created:
            print(f"✅ Created message: {sender.username} → {receiver.username}")
    
    print(f"\n=== Test Data Summary ===")
    print(f"Total users: {User.objects.count()}")
    print(f"Total friendships: {Friendship.objects.count()}")
    print(f"Total messages: {Message.objects.count()}")
    
    print(f"\n=== Login Information ===")
    for user in created_users:
        print(f"Username: {user.username}, Password: password123")
    
    # Test conversation retrieval for Alice
    print(f"\n=== Alice's Conversations ===")
    conversations = Message.get_recent_conversations(alice)
    for conv in conversations:
        print(f"- {conv['user'].get_full_name()}: {conv['last_message'].content[:50]}...")
        print(f"  Unread: {conv['unread_count']}")

if __name__ == "__main__":
    create_test_messaging_data()