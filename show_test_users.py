#!/usr/bin/env python
"""
Script to test the red notification bell by logging into accounts with unread notifications
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def show_users_with_unread_notifications():
    """Show users that have unread notifications for testing"""
    print("=== Users with Unread Notifications (for testing red bell) ===\n")
    
    users = User.objects.all()
    test_users = []
    
    for user in users:
        unread_count = user.user_notifications.filter(is_read=False).count()
        if unread_count > 0:
            test_users.append((user, unread_count))
            
    if not test_users:
        print("No users with unread notifications found.")
        return
        
    print("You can test the red notification bell with any of these users:")
    print("(Username | Unread Count | Login URL)")
    print("-" * 60)
    
    for user, count in test_users:
        print(f"{user.username:<15} | {count:>5} unread | http://127.0.0.1:8000/users/login/")
        
        # Show recent unread notifications
        recent_notifications = user.user_notifications.filter(is_read=False)[:3]
        if recent_notifications:
            print(f"  Recent notifications:")
            for notif in recent_notifications:
                print(f"    - {notif.title}")
        print()
    
    print("\n=== Testing Instructions ===")
    print("1. Go to: http://127.0.0.1:8000/users/login/")
    print("2. Login with any username from the list above")
    print("3. Check if the notification bell is RED")
    print("4. The bell should show the unread count")
    print("5. Click on notifications to view them")
    print("6. Mark notifications as read to see the bell turn GREEN")
    print("\nNote: Use password 'testpass123' for testuser, or try common passwords")

if __name__ == "__main__":
    show_users_with_unread_notifications()
