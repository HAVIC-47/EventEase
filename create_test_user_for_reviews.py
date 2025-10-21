#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    """Create a simple test user for testing review submission"""
    
    # Check if user already exists
    username = 'testuser'
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"User '{username}' already exists")
    else:
        # Create new user
        user = User.objects.create_user(
            username=username,
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"Created user '{username}' with password 'testpass123'")
    
    print(f"You can now login with:")
    print(f"Username: {username}")
    print(f"Password: testpass123")
    print(f"Go to: http://127.0.0.1:8000/auth/login/")
    print(f"Then visit: http://127.0.0.1:8000/reviews/submit/")

if __name__ == '__main__':
    create_test_user()