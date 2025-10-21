#!/usr/bin/env python
"""
Test script for venue rating system functionality with venue bookings
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
from venues.models import Venue, VenueBooking
from reviews.models import VenueReview
from django.utils import timezone
from datetime import timedelta, date

User = get_user_model()

def test_venue_booking_review_system():
    print("🏢 Testing Venue Booking Review System...")
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='venue_booker',
        defaults={
            'email': 'venue_booker@test.com',
            'first_name': 'Venue',
            'last_name': 'Booker'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Using existing test user: {user.username}")
    
    # Get or create test venue
    venue = Venue.objects.filter(name__icontains='Test Booking Venue').first()
    if not venue:
        venue = Venue.objects.create(
            name='Test Booking Venue for Reviews',
            description='A venue for testing booking reviews',
            address='456 Booking Street',
            city='Test City',
            state='TC',
            zipcode='12345',
            country='Test Country',
            capacity=150,
            venue_type='conference_center',
            price_per_hour=75.00,
            is_available=True,
            manager=user  # Add manager requirement
        )
        print(f"✅ Created test venue: {venue.name}")
    else:
        print(f"✅ Using existing test venue: {venue.name}")
    
    # Create a completed venue booking (past booking)
    booking = VenueBooking.objects.filter(venue=venue, user=user).first()
    if not booking:
        booking = VenueBooking.objects.create(
            venue=venue,
            user=user,
            event_title='Test Conference for Reviews',
            event_description='A test conference to verify venue reviews',
            start_date=timezone.now() - timedelta(days=7),  # Past start date
            end_date=timezone.now() - timedelta(days=6),    # Past end date
            total_amount=600.00,
            status='completed',  # Completed booking
            contact_email=user.email,
            contact_phone='555-0123',
            special_requirements='Please test venue reviews'
        )
        print(f"✅ Created completed venue booking: {booking.id}")
    else:
        # Ensure booking is completed and in the past
        booking.status = 'completed'
        booking.start_date = timezone.now() - timedelta(days=7)
        booking.end_date = timezone.now() - timedelta(days=6)
        booking.save()
        print(f"✅ Updated existing venue booking: {booking.id}")
    
    # Test venue rating properties before any reviews
    print(f"\n📊 Venue stats before reviews:")
    print(f"   Average Rating: {venue.average_rating}")
    print(f"   Review Count: {venue.review_count}")
    print(f"   Category Averages: {venue.category_averages}")
    
    # Test booking validation - user should be able to review
    print(f"\n🔍 Testing booking validation:")
    print(f"   User: {user.username}")
    print(f"   Venue: {venue.name}")
    print(f"   Booking Status: {booking.status}")
    print(f"   Booking End Date: {booking.end_date}")
    print(f"   Today's Date: {date.today()}")
    print(f"   Booking Completed: {booking.end_date < timezone.now()}")
    
    # Create test venue review
    review, created = VenueReview.objects.get_or_create(
        venue=venue,
        user=user,
        defaults={
            'rating': 5,
            'ambience_rating': 5,
            'service_rating': 4,
            'cleanliness_rating': 5,
            'value_rating': 4,
            'title': 'Excellent venue for conferences!',
            'comment': 'Amazing venue with great facilities. Perfect ambience for professional events, excellent service throughout our conference. Very clean and well-maintained. Good value for the money.'
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
    
    # Test review validation for non-booker
    print(f"\n🔒 Testing review validation:")
    
    # Create another user without bookings
    user2, created = User.objects.get_or_create(
        username='non_booker',
        defaults={
            'email': 'non_booker@test.com',
            'first_name': 'Non',
            'last_name': 'Booker'
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
            comment='Trying to review without booking'
        )
        invalid_review.full_clean()  # This should raise ValidationError
        print("❌ Validation failed - non-booker was able to create review")
    except django.core.exceptions.ValidationError as e:
        print(f"✅ Validation working - {e}")
    
    # Test user with future booking (should not be able to review)
    future_booking = VenueBooking.objects.create(
        venue=venue,
        user=user2,
        event_title='Future Conference',
        event_description='A future conference booking',
        start_date=timezone.now() + timedelta(days=7),  # Future start date
        end_date=timezone.now() + timedelta(days=8),    # Future end date
        total_amount=700.00,
        status='confirmed',  # Confirmed but not completed
        contact_email=user2.email,
        contact_phone='555-0456'
    )
    
    try:
        # This should also fail validation (booking not completed)
        future_review = VenueReview(
            venue=venue,
            user=user2,
            rating=4,
            ambience_rating=4,
            service_rating=4,
            cleanliness_rating=4,
            value_rating=4,
            title='Future booking review',
            comment='Trying to review before booking is completed'
        )
        future_review.full_clean()  # This should raise ValidationError
        print("❌ Validation failed - user with future booking was able to create review")
    except django.core.exceptions.ValidationError as e:
        print(f"✅ Validation working for future booking - {e}")
    
    print(f"\n🎉 Venue booking review system test completed successfully!")
    print(f"   Venue: {venue.name}")
    print(f"   Average Rating: {venue.average_rating}/5")
    print(f"   Total Reviews: {venue.review_count}")
    print(f"   Total Bookings: {VenueBooking.objects.filter(venue=venue).count()}")
    
    return venue, review, booking

if __name__ == '__main__':
    test_venue_booking_review_system()