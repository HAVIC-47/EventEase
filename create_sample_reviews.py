#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from reviews.models import Review

def create_sample_reviews():
    """Create sample reviews for testing"""
    
    # Sample review data
    sample_reviews = [
        {
            'username': 'priom',
            'rating': 5,
            'title': 'Outstanding Event Management!',
            'content': 'EventEase made organizing our corporate event incredibly smooth. The platform is intuitive and the venue booking process was seamless. Highly recommend!'
        },
        {
            'username': 'nusaiba',
            'rating': 5,
            'title': 'Love the Experience!',
            'content': 'I attended several events through EventEase and every single one was well-organized. The booking system is user-friendly and the events are always top quality.'
        },
        {
            'username': 'sharif',
            'rating': 4,
            'title': 'Great Platform for Tech Events',
            'content': 'As a tech enthusiast, I found EventEase to be the perfect platform for discovering and attending tech meetups and conferences. The variety is impressive!'
        },
        {
            'username': 'admin',
            'rating': 5,
            'title': 'Perfect Solution for Event Management',
            'content': 'From the organizer perspective, EventEase provides everything needed to manage events efficiently. The venue integration and booking system work flawlessly.'
        }
    ]
    
    created_count = 0
    
    for review_data in sample_reviews:
        try:
            # Get or create user
            user = User.objects.filter(username=review_data['username']).first()
            if not user:
                print(f"User {review_data['username']} not found, skipping review")
                continue
                
            # Check if review already exists
            if Review.objects.filter(user=user).exists():
                print(f"Review for {review_data['username']} already exists, skipping")
                continue
                
            # Create review
            review = Review.objects.create(
                user=user,
                rating=review_data['rating'],
                title=review_data['title'],
                content=review_data['content']
            )
            
            print(f"Created review for {user.get_full_name() or user.username}")
            created_count += 1
            
        except Exception as e:
            print(f"Error creating review for {review_data['username']}: {e}")
    
    print(f"\nTotal reviews created: {created_count}")
    print(f"Total reviews in database: {Review.objects.count()}")

if __name__ == '__main__':
    create_sample_reviews()