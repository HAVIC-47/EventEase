#!/usr/bin/env python
"""
Test venue review submission for specific failing user to verify the fix.
"""

import os
import sys
import django
from datetime import datetime, timedelta, date
from django.utils import timezone

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from venues.models import Venue, VenueBooking
from reviews.models import VenueReview
from django.test import Client

def test_fixed_venue_review_submission():
    """
    Test the fixed venue review submission for users who were failing before.
    """
    print("🔧 Testing Fixed Venue Review Submission...")
    print("=" * 60)
    
    # Test cases that were failing before with status 302
    failing_cases = [
        (2, 'Akhi_1'),    # UAP venue - multiple bookings
        (9, 'reviewer1'), # Grand Ballroom - completed status
        (10, 'reviewer2'), # Modern Conference Center - completed status
    ]
    
    client = Client()
    
    for venue_id, username in failing_cases:
        print(f"\n🎯 Testing Venue ID: {venue_id} with User: {username}")
        
        try:
            venue = Venue.objects.get(id=venue_id)
            user = User.objects.get(username=username)
            
            print(f"   🏢 Venue: {venue.name}")
            print(f"   👤 User: {user.username}")
            
            # Check if user already has a review (to avoid duplicates)
            existing_review = VenueReview.objects.filter(venue=venue, user=user).first()
            if existing_review:
                print(f"   ✅ User already has review (Rating: {existing_review.rating}/5)")
                continue
            
            # Login and test review submission page
            client.force_login(user)
            
            review_url = f'/reviews/venue/{venue_id}/submit/'
            print(f"   🔗 Testing URL: {review_url}")
            
            # Test GET request (should show form)
            get_response = client.get(review_url)
            print(f"   📄 GET Status: {get_response.status_code}")
            
            if get_response.status_code == 200:
                print(f"   ✅ Review form accessible!")
                
                # Test POST request (submit review)
                review_data = {
                    'rating': 4,
                    'ambience_rating': 4,
                    'service_rating': 4,
                    'cleanliness_rating': 4,
                    'value_rating': 4,
                    'title': f'Fixed test review for {venue.name}',
                    'comment': f'This is a test review after fixing the VenueBooking validation issue.'
                }
                
                post_response = client.post(review_url, review_data)
                print(f"   📝 POST Status: {post_response.status_code}")
                
                if post_response.status_code == 302:  # Redirect after successful submission
                    # Check if review was actually created
                    new_review = VenueReview.objects.filter(venue=venue, user=user).first()
                    if new_review:
                        print(f"   🎉 SUCCESS! Review created with rating: {new_review.rating}/5")
                        print(f"   📝 Review title: {new_review.title}")
                    else:
                        print(f"   ❌ POST redirected but no review found in database")
                elif post_response.status_code == 200:
                    content = post_response.content.decode('utf-8')
                    if 'error' in content.lower():
                        print(f"   ❌ Form errors in response")
                    else:
                        print(f"   ⚠️ Form returned with data (check for validation issues)")
                else:
                    print(f"   ❌ POST request failed")
                    
            elif get_response.status_code == 302:
                print(f"   ❌ Still redirecting - validation issue not fixed")
            else:
                print(f"   ❌ GET request failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 60)
    
    # Summary of reviews created
    print(f"\n📊 Final Review Summary:")
    for venue_id, username in failing_cases:
        try:
            venue = Venue.objects.get(id=venue_id)
            user = User.objects.get(username=username)
            review = VenueReview.objects.filter(venue=venue, user=user).first()
            
            if review:
                print(f"   ✅ {venue.name} - {user.username}: {review.rating}/5 stars")
            else:
                print(f"   ❌ {venue.name} - {user.username}: No review")
        except:
            pass

if __name__ == '__main__':
    test_fixed_venue_review_submission()