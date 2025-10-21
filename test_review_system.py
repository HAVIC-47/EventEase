#!/usr/bin/env python
"""
Test script to verify the event review system functionality
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking
from reviews.models import EventReview

def test_review_system():
    """Test the event review system"""
    print("🚀 Testing Event Review System...")
    
    # Create a test user if doesn't exist
    test_user, created = User.objects.get_or_create(
        username='review_tester',
        defaults={
            'email': 'reviewer@test.com',
            'first_name': 'Review',
            'last_name': 'Tester'
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Using existing test user: {test_user.username}")
    
    # Create a test event organizer
    organizer, created = User.objects.get_or_create(
        username='event_organizer',
        defaults={
            'email': 'organizer@test.com',
            'first_name': 'Event',
            'last_name': 'Organizer'
        }
    )
    if created:
        organizer.set_password('testpass123')
        organizer.save()
        print(f"✅ Created organizer: {organizer.username}")
    
    # Create a past event for testing
    past_date = timezone.now() - timedelta(days=7)
    end_date = past_date + timedelta(hours=3)
    
    event, created = Event.objects.get_or_create(
        title='Test Review Event',
        defaults={
            'description': 'This is a test event for reviewing system',
            'event_type': 'conference',
            'organizer': organizer,
            'venue_name': 'Test Venue',
            'venue_address': '123 Test Street, Test City',
            'start_date': past_date,
            'end_date': end_date,
            'contact_email': 'test@example.com',
            'ticket_price': 50.00,
            'is_free': False,
            'max_attendees': 100,
        }
    )
    if created:
        print(f"✅ Created test event: {event.title}")
    else:
        print(f"✅ Using existing test event: {event.title}")
    
    # Create a confirmed booking for the user
    booking, created = EventBooking.objects.get_or_create(
        user=test_user,
        event=event,
        defaults={
            'attendees_count': 1,
            'total_amount': event.ticket_price,
            'status': 'confirmed',
            'attendee_name': f"{test_user.first_name} {test_user.last_name}",
            'attendee_email': test_user.email,
            'attendee_phone': '123-456-7890',
        }
    )
    if created:
        print(f"✅ Created test booking: {booking.id}")
    else:
        print(f"✅ Using existing test booking: {booking.id}")
    
    # Test event review functionality
    print("\n📝 Testing Review Model...")
    
    # Check if event can be reviewed
    print(f"📅 Event status: {event.status}")
    print(f"📋 Event can be reviewed: {event.can_be_reviewed}")
    print(f"⭐ Current average rating: {event.average_rating}")
    print(f"📊 Current review count: {event.review_count}")
    
    # Test EventReview model
    existing_review = EventReview.objects.filter(event=event, user=test_user).first()
    if existing_review:
        print(f"✅ Existing review found: {existing_review.title} - {existing_review.rating}/5")
    else:
        print("📝 No existing review found")
        
        # Create a test review
        try:
            test_review = EventReview(
                event=event,
                user=test_user,
                title='Great Conference!',
                comment='This event was really well organized and informative.',
                rating=5,
                organization_rating=5,
                venue_rating=4,
                value_rating=4
            )
            test_review.full_clean()  # This will run validation
            test_review.save()
            print(f"✅ Created test review: {test_review.title}")
            
            # Check updated event stats
            print(f"⭐ Updated average rating: {event.average_rating}")
            print(f"📊 Updated review count: {event.review_count}")
            
        except Exception as e:
            print(f"❌ Error creating review: {e}")
    
    # Test review permissions
    print("\n🔐 Testing Review Permissions...")
    
    # Create another user who didn't attend
    non_attendee, created = User.objects.get_or_create(
        username='non_attendee',
        defaults={
            'email': 'nonattendee@test.com',
            'first_name': 'Non',
            'last_name': 'Attendee'
        }
    )
    
    # Try to create review as non-attendee (should fail)
    try:
        invalid_review = EventReview(
            event=event,
            user=non_attendee,
            title='Fake Review',
            comment='I did not attend this event.',
            rating=1,
            organization_rating=1,
            venue_rating=1,
            value_rating=1
        )
        invalid_review.full_clean()
        print("❌ Non-attendee was allowed to review (this should not happen)")
    except Exception as e:
        print(f"✅ Non-attendee correctly blocked from reviewing: {e}")
    
    print("\n🎉 Review system test completed!")
    return True

if __name__ == '__main__':
    test_review_system()