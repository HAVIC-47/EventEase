#!/usr/bin/env python
"""
Simple script to test the notification API endpoint
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_notification_api():
    """Test the notification count API"""
    client = Client()
    
    # Test with users that have unread notifications
    test_users = ['testuser', 'demo_user', 'test_customer']
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            
            # Login as the user
            client.force_login(user)
            
            # Call the API
            response = client.get('/notifications/api/count/')
            
            print(f"User: {username}")
            print(f"  Status Code: {response.status_code}")
            print(f"  Response: {response.content.decode()}")
            print(f"  Actual unread count: {user.user_notifications.filter(is_read=False).count()}")
            print()
            
        except User.DoesNotExist:
            print(f"User {username} not found")
        except Exception as e:
            print(f"Error testing {username}: {e}")

if __name__ == "__main__":
    test_notification_api()
