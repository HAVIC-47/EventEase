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
from reviews.models import Review

def create_additional_reviews():
    """Create additional sample reviews for testing"""
    
    # Get existing users
    users = User.objects.all()
    print(f"Found {users.count()} users in database")
    
    # Sample reviews data
    additional_reviews = [
        {
            'title': 'Excellent Event Management',
            'content': 'EventEase has transformed how we organize our company events. The booking system is intuitive and the venue recommendations are spot-on. Highly recommended!',
            'rating': 5
        },
        {
            'title': 'Great Platform with Room for Improvement',
            'content': 'The event discovery feature is fantastic and helped us find the perfect venue. The payment integration could be smoother, but overall a solid platform.',
            'rating': 4
        },
        {
            'title': 'User-Friendly Interface',
            'content': 'Love how easy it is to browse events and make bookings. The notification system keeps me updated on all my event activities. Great work!',
            'rating': 5
        },
        {
            'title': 'Good Service, Fast Response',
            'content': 'Customer support is responsive and helpful. The venue filtering options are comprehensive. Would definitely use again for future events.',
            'rating': 4
        },
        {
            'title': 'Innovative Event Solutions',
            'content': 'EventEase provides innovative solutions for event management. The analytics dashboard gives great insights into event performance.',
            'rating': 5
        }
    ]
    
    # Create reviews for different users
    created_count = 0
    for i, review_data in enumerate(additional_reviews):
        if i < len(users):
            user = users[i]
            
            # Check if user already has a recent review with similar title
            existing_review = Review.objects.filter(
                user=user,
                title=review_data['title']
            ).first()
            
            if not existing_review:
                review = Review.objects.create(
                    user=user,
                    title=review_data['title'],
                    content=review_data['content'],
                    rating=review_data['rating']
                )
                print(f"Created review '{review.title}' for {user.get_full_name() or user.username}")
                created_count += 1
            else:
                print(f"Review '{review_data['title']}' already exists for {user.get_full_name() or user.username}")
    
    # Display summary
    total_reviews = Review.objects.count()
    print(f"\nTotal new reviews created: {created_count}")
    print(f"Total reviews in database: {total_reviews}")
    
    # Show all reviews
    print("\nAll reviews in database:")
    for review in Review.objects.all().order_by('-created_at'):
        print(f"- {review.title} ({review.rating}⭐) by {review.user.get_full_name() or review.user.username}")

if __name__ == '__main__':
    create_additional_reviews()