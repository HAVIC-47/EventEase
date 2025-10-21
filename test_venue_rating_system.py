#!/usr/bin/env python
"""
Test script for venue rating system functionality
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth import get_user_model
from venues.models import Venue
from reviews.models import VenueReview
from events.models import Event, EventBooking
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def test_venue_rating_system():
    print("🏢 Testing Venue Rating System...")
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='venue_reviewer',
        defaults={
            'email': 'venue_reviewer@test.com',
            'first_name': 'Venue',
            'last_name': 'Reviewer'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Using existing test user: {user.username}")
    
    # Get or create test venue
    venue = Venue.objects.filter(name__icontains='Test Venue').first()
    if not venue:
        venue = Venue.objects.create(
            name='Test Venue for Ratings',
            description='A beautiful venue for testing ratings',
            address='123 Test Street',
            city='Test City',
            state='TC',
            zipcode='12345',
            country='Test Country',
            capacity=100,
            venue_type='conference_center',
            price_per_hour=50.00,
            is_available=True
        )
        print(f"✅ Created test venue: {venue.name}")
    else:
        print(f"✅ Using existing test venue: {venue.name}")
    
    # Create test event at the venue
    event = Event.objects.filter(venue=venue, title__icontains='Test Event').first()
    if not event:
        event = Event.objects.create(
            title='Test Event at Venue',
            description='Test event for venue rating',
            venue=venue,
            organizer=user,
            start_date=timezone.now() - timedelta(days=1),  # Past event
            end_date=timezone.now() - timedelta(hours=22),
            ticket_price=25.00,
            max_attendees=50,
            event_type='conference',
            contact_email='test@example.com',
            venue_address='123 Test Street, Test City'
        )
        print(f"✅ Created test event: {event.title}")
    else:
        print(f"✅ Using existing test event: {event.title}")
    
    # Create confirmed booking for user
    booking, created = EventBooking.objects.get_or_create(
        event=event,
        user=user,
        defaults={
            'attendees_count': 1,
            'total_amount': event.ticket_price,
            'amount': event.ticket_price,
            'status': 'confirmed'
        }
    )
    if created:
        print(f"✅ Created test booking: {booking.id}")
    else:
        # Ensure booking is confirmed
        booking.status = 'confirmed'
        booking.save()
        print(f"✅ Using existing test booking: {booking.id}")
    
    # Test venue rating properties before any reviews
    print(f"\n📊 Venue stats before reviews:")
    print(f"   Average Rating: {venue.average_rating}")
    print(f"   Review Count: {venue.review_count}")
    print(f"   Category Averages: {venue.category_averages}")
    
    # Create test venue review
    review, created = VenueReview.objects.get_or_create(
        venue=venue,
        user=user,
        defaults={
            'rating': 4,
            'ambience_rating': 5,
            'service_rating': 4,
            'cleanliness_rating': 4,
            'value_rating': 3,
            'title': 'Great venue experience!',
            'comment': 'Great venue! Beautiful ambience and excellent service. Clean facilities and good value for money.'
        }
    )
    
    if created:
        print(f"✅ Created venue review with rating: {review.rating}/5")
    else:
        print(f"✅ Venue review already exists with rating: {review.rating}/5")
    
    # Refresh venue from database to get updated ratings
    venue.refresh_from_db()
    
    # Test venue rating properties after review
    print(f"\n📊 Venue stats after review:")
    print(f"   Average Rating: {venue.average_rating}")
    print(f"   Review Count: {venue.review_count}")
    print(f"   Category Averages: {venue.category_averages}")
    
    # Test venue review properties
    print(f"\n⭐ Review details:")
    print(f"   Overall: {review.rating}/5")
    print(f"   Ambience: {review.ambience_rating}/5")
    print(f"   Service: {review.service_rating}/5")
    print(f"   Cleanliness: {review.cleanliness_rating}/5")
    print(f"   Value: {review.value_rating}/5")
    print(f"   Title: {review.title}")
    print(f"   Review Text: {review.comment[:100]}...")
    
    # Test review validation
    print(f"\n🔒 Testing review validation:")
    
    # Create another user without attendance
    user2, created = User.objects.get_or_create(
        username='non_attendee',
        defaults={
            'email': 'non_attendee@test.com',
            'first_name': 'Non',
            'last_name': 'Attendee'
        }
    )
    
    try:
        # This should fail validation
        invalid_review = VenueReview(
            venue=venue,
            user=user2,
            rating=5,
            ambience_rating=5,
            service_rating=5,
            cleanliness_rating=5,
            value_rating=5,
            title='Invalid review',
            comment='Trying to review without attending'
        )
        invalid_review.full_clean()  # This should raise ValidationError
        print("❌ Validation failed - non-attendee was able to create review")
    except django.core.exceptions.ValidationError as e:
        print(f"✅ Validation working - {e}")
    
    print(f"\n🎉 Venue rating system test completed successfully!")
    print(f"   Venue: {venue.name}")
    print(f"   Average Rating: {venue.average_rating}/5")
    print(f"   Total Reviews: {venue.review_count}")
    
    return venue, review

if __name__ == '__main__':
    test_venue_rating_system()