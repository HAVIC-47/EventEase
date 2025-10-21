#!/usr/bin/env python
"""
Test the fixed review submission functionality
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
from reviews.forms import EventReviewForm

def test_fixed_review_form():
    """Test that the EventReviewForm now works correctly with event and user"""
    print("🔧 Testing Fixed Review Form...")
    
    # Get existing test data
    try:
        test_user = User.objects.get(username='review_tester')
        event = Event.objects.get(title='Test Review Event')
        booking = EventBooking.objects.filter(user=test_user, event=event).first()
        
        print(f"✅ Found test user: {test_user.username}")
        print(f"✅ Found test event: {event.title}")
        print(f"✅ Found test booking: {booking.id if booking else 'None'}")
        
        # Test form creation with event and user
        form_data = {
            'rating': 4,
            'organization_rating': 4,
            'venue_rating': 5,
            'value_rating': 3,
            'title': 'Fixed Review Test',
            'comment': 'Testing the fixed review form functionality.'
        }
        
        # Delete existing review if any for clean test
        existing_review = EventReview.objects.filter(event=event, user=test_user).first()
        if existing_review:
            existing_review.delete()
            print("🗑️ Deleted existing review for clean test")
        
        # Test form initialization
        form = EventReviewForm(data=form_data, event=event, user=test_user)
        print(f"📝 Form created with event and user")
        
        # Test form validation
        if form.is_valid():
            print("✅ Form is valid")
            
            # Test form save
            try:
                review = form.save()
                print(f"✅ Review saved successfully: {review.title}")
                print(f"⭐ Rating: {review.rating}/5")
                print(f"🎯 Event: {review.event.title}")
                print(f"👤 User: {review.user.username}")
                
                # Verify the review was saved properly
                saved_review = EventReview.objects.get(id=review.id)
                print(f"✅ Verification: Review {saved_review.id} exists in database")
                
                return True
                
            except Exception as e:
                print(f"❌ Error saving review: {e}")
                return False
        else:
            print(f"❌ Form validation failed: {form.errors}")
            return False
            
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False

def test_review_model_validation():
    """Test the updated model validation"""
    print("\n🔍 Testing Updated Model Validation...")
    
    try:
        test_user = User.objects.get(username='review_tester')
        event = Event.objects.get(title='Test Review Event')
        
        # Test creating review instance without validation issues
        review = EventReview(
            event=event,
            user=test_user,
            title='Validation Test',
            comment='Testing model validation',
            rating=5,
            organization_rating=5,
            venue_rating=4,
            value_rating=4
        )
        
        # This should not raise the RelatedObjectDoesNotExist error anymore
        try:
            review.full_clean()
            print("✅ Model validation passed")
            return True
        except Exception as e:
            print(f"❌ Model validation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Model validation test setup failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Testing Fixed Review System...")
    
    form_test = test_fixed_review_form()
    model_test = test_review_model_validation()
    
    if form_test and model_test:
        print("\n🎉 All tests passed! Review system is now working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check the output above.")