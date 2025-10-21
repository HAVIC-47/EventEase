#!/usr/bin/env python
"""
Test venue review functionality across multiple venues to identify issues.
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
from django.urls import reverse

def test_venue_review_across_all_venues():
    """
    Test venue review functionality across all venues with completed bookings.
    """
    print("🔍 Testing Venue Review Functionality Across All Venues...")
    print("=" * 70)
    
    # Get all venues with completed bookings
    venues_with_bookings = []
    
    for venue in Venue.objects.all().order_by('id'):
        completed_bookings = VenueBooking.objects.filter(
            venue=venue,
            status__in=['confirmed', 'completed'], 
            end_date__lt=timezone.now()
        )
        
        if completed_bookings.exists():
            venues_with_bookings.append((venue, completed_bookings))
    
    print(f"Found {len(venues_with_bookings)} venues with completed bookings")
    print()
    
    client = Client()
    
    for venue, completed_bookings in venues_with_bookings:
        print(f"🏢 Testing Venue: {venue.name} (ID: {venue.id})")
        print(f"   Type: {venue.venue_type}")
        print(f"   Manager: {venue.manager.username if venue.manager else 'None'}")
        print(f"   Completed Bookings: {completed_bookings.count()}")
        
        # Test each user who has completed a booking
        for booking in completed_bookings:
            user = booking.user
            print(f"\n   👤 Testing User: {user.username}")
            print(f"      Booking ID: {booking.id}")
            print(f"      Booking Status: {booking.status}")
            print(f"      End Date: {booking.end_date}")
            
            # Check if user already has a review
            existing_review = VenueReview.objects.filter(venue=venue, user=user).first()
            if existing_review:
                print(f"      ✅ User already has review (Rating: {existing_review.rating}/5)")
                continue
                
            print(f"      🎯 User can potentially review - Testing review creation...")
            
            # Login as this user
            client.force_login(user)
            
            # Test 1: Check dashboard shows review button
            dashboard_response = client.get('/auth/dashboard/')
            if dashboard_response.status_code == 200:
                dashboard_content = dashboard_response.content.decode('utf-8')
                if venue.name in dashboard_content:
                    if 'Leave Review' in dashboard_content:
                        print(f"      ✅ Dashboard shows 'Leave Review' button")
                    elif 'View Your Review' in dashboard_content:
                        print(f"      ✅ Dashboard shows 'View Your Review' button")
                    else:
                        print(f"      ❌ Dashboard doesn't show review button")
                else:
                    print(f"      ❌ Venue not found in dashboard")
            else:
                print(f"      ❌ Dashboard failed to load (Status: {dashboard_response.status_code})")
            
            # Test 2: Check venue detail page shows review button
            venue_detail_response = client.get(f'/venues/{venue.id}/')
            if venue_detail_response.status_code == 200:
                venue_content = venue_detail_response.content.decode('utf-8')
                # Look for the correct button texts
                review_buttons = [
                    'Write a Review',
                    'Write the First Review', 
                    'Edit Your Review',
                    'Add Review',
                    'Leave Review'
                ]
                
                button_found = any(button in venue_content for button in review_buttons)
                if button_found:
                    found_button = next(button for button in review_buttons if button in venue_content)
                    print(f"      ✅ Venue detail shows review button: '{found_button}'")
                else:
                    print(f"      ❌ Venue detail doesn't show review button")
            else:
                print(f"      ❌ Venue detail failed to load (Status: {venue_detail_response.status_code})")
            
            # Test 3: Try to access review submission page
            review_submit_url = f'/reviews/venue/{venue.id}/submit/'
            review_response = client.get(review_submit_url)
            print(f"      🔗 Review submission URL: {review_submit_url}")
            print(f"      📄 Review page status: {review_response.status_code}")
            
            if review_response.status_code == 200:
                print(f"      ✅ Review submission page accessible")
                
                # Test actual review submission
                review_data = {
                    'rating': 4,
                    'ambience_rating': 4,
                    'service_rating': 4,
                    'cleanliness_rating': 4,
                    'value_rating': 4,
                    'title': f'Test review for {venue.name}',
                    'comment': f'This is a test review for {venue.name} by {user.username}.'
                }
                
                submit_response = client.post(review_submit_url, review_data)
                print(f"      📝 Review submission status: {submit_response.status_code}")
                
                if submit_response.status_code == 302:  # Redirect after successful submission
                    # Check if review was created
                    new_review = VenueReview.objects.filter(venue=venue, user=user).first()
                    if new_review:
                        print(f"      ✅ Review successfully created! (Rating: {new_review.rating}/5)")
                    else:
                        print(f"      ❌ Review submission redirected but no review found in database")
                elif submit_response.status_code == 200:
                    # Check for form errors
                    response_content = submit_response.content.decode('utf-8')
                    if 'error' in response_content.lower() or 'invalid' in response_content.lower():
                        print(f"      ❌ Review submission failed with form errors")
                    else:
                        print(f"      ⚠️ Review submission returned 200 (check for form issues)")
                else:
                    print(f"      ❌ Review submission failed")
                    
            elif review_response.status_code == 302:
                print(f"      ⚠️ Review page redirected (might be login redirect)")
            elif review_response.status_code == 403:
                print(f"      ❌ Review page forbidden (validation working)")
            elif review_response.status_code == 404:
                print(f"      ❌ Review page not found (URL issue)")
            else:
                print(f"      ❌ Review page error")
        
        print(f"\n   📊 Current venue stats:")
        venue_reviews = VenueReview.objects.filter(venue=venue)
        print(f"   Total Reviews: {venue_reviews.count()}")
        if venue_reviews.exists():
            avg_rating = sum(r.rating for r in venue_reviews) / venue_reviews.count()
            print(f"   Average Rating: {avg_rating:.1f}/5")
        
        print("-" * 70)
    
    print(f"\n🎉 Venue Review Testing Complete!")
    print(f"Tested {len(venues_with_bookings)} venues with completed bookings")

if __name__ == '__main__':
    test_venue_review_across_all_venues()
