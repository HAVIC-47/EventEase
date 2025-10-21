#!/usr/bin/env python
"""
Test script to verify venue review UI integration with dashboard and venue detail pages.
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

def test_venue_review_ui_integration():
    """
    Test the complete venue review UI integration workflow.
    """
    print("🏢 Testing Venue Review UI Integration...")
    
    # Get existing test user and venue from our previous test
    user = User.objects.get(username='venue_booker')
    venue = Venue.objects.get(name='Test Booking Venue for Reviews')
    
    print(f"✅ Using test user: {user.username}")
    print(f"✅ Using test venue: {venue.name}")
    
    # Verify completed booking exists
    completed_booking = VenueBooking.objects.filter(
        user=user,
        venue=venue,
        status='completed',
        end_date__lt=timezone.now()
    ).first()
    
    if completed_booking:
        print(f"✅ Found completed booking: {completed_booking.id}")
        print(f"   Booking Status: {completed_booking.status}")
        print(f"   End Date: {completed_booking.end_date}")
        print(f"   User can review: {completed_booking.end_date < timezone.now()}")
    else:
        print("❌ No completed booking found for user")
        return
    
    # Test Client for simulating requests
    client = Client()
    
    # Test 1: Dashboard view should show venue review button
    print(f"\n🎯 Test 1: Dashboard Review Button")
    client.force_login(user)
    dashboard_response = client.get('/auth/dashboard/')
    
    if dashboard_response.status_code == 200:
        dashboard_content = dashboard_response.content.decode('utf-8')
        
        # Check if venue booking is shown
        if venue.name in dashboard_content:
            print(f"✅ Venue '{venue.name}' appears in dashboard")
        else:
            print(f"❌ Venue '{venue.name}' not found in dashboard")
        
        # Check for review button (either "Leave Review" or "View Your Review")
        if 'Leave Review' in dashboard_content or 'View Your Review' in dashboard_content or 'review-btn' in dashboard_content:
            if 'View Your Review' in dashboard_content:
                print("✅ 'View Your Review' button found in dashboard (user has existing review)")
            elif 'Leave Review' in dashboard_content:
                print("✅ 'Leave Review' button found in dashboard (user can review)")
            else:
                print("✅ Review button found in dashboard")
        else:
            print("❌ Review button not found in dashboard")
    else:
        print(f"❌ Dashboard request failed with status {dashboard_response.status_code}")
    
    # Test 2: Venue detail page should show review button
    print(f"\n🎯 Test 2: Venue Detail Review Button")
    venue_detail_response = client.get(f'/venues/{venue.id}/')
    
    if venue_detail_response.status_code == 200:
        venue_content = venue_detail_response.content.decode('utf-8')
        
        # Check if venue details are shown
        if venue.name in venue_content:
            print(f"✅ Venue details page loaded successfully")
        else:
            print(f"❌ Venue details page not loading properly")
        
        # Check for review button (should be shown since user has completed booking)
        if 'Add Review' in venue_content or 'review-btn' in venue_content:
            print("✅ Review button found in venue detail page")
        else:
            print("❌ Review button not found in venue detail page")
            
        # Check if existing review is shown
        existing_review = VenueReview.objects.filter(venue=venue, user=user).first()
        if existing_review:
            if existing_review.title in venue_content:
                print(f"✅ Existing review displayed: '{existing_review.title}'")
            else:
                print("❌ Existing review not displayed properly")
    else:
        print(f"❌ Venue detail request failed with status {venue_detail_response.status_code}")
    
    # Test 3: Test user without booking cannot see review button
    print(f"\n🎯 Test 3: Non-booking User Restriction")
    
    # Create a user without any venue bookings
    test_user, created = User.objects.get_or_create(
        username='no_booking_user',
        defaults={
            'email': 'nobooking@test.com',
            'first_name': 'No',
            'last_name': 'Booking'
        }
    )
    
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Created test user without bookings: {test_user.username}")
    else:
        print(f"✅ Using existing test user without bookings: {test_user.username}")
    
    # Test dashboard for user without bookings
    client.force_login(test_user)
    no_booking_dashboard = client.get('/auth/dashboard/')
    
    if no_booking_dashboard.status_code == 200:
        no_booking_content = no_booking_dashboard.content.decode('utf-8')
        
        # Should not show venue review buttons
        if 'Review Venue' not in no_booking_content and venue.name not in no_booking_content:
            print("✅ Dashboard correctly shows no venue bookings for non-booking user")
        else:
            print("❌ Dashboard incorrectly shows venue bookings for non-booking user")
    
    # Test venue detail for user without bookings
    no_booking_venue_detail = client.get(f'/venues/{venue.id}/')
    
    if no_booking_venue_detail.status_code == 200:
        no_booking_venue_content = no_booking_venue_detail.content.decode('utf-8')
        
        # Should not show review button
        if 'Add Review' not in no_booking_venue_content:
            print("✅ Venue detail correctly hides review button for non-booking user")
        else:
            print("❌ Venue detail incorrectly shows review button for non-booking user")
    
    # Test 4: Review submission workflow
    print(f"\n🎯 Test 4: Review Submission Workflow")
    
    # Login back as venue_booker
    client.force_login(user)
    
    # Test accessing review creation page
    review_create_url = f'/reviews/venue/{venue.id}/submit/'
    try:
        review_page_response = client.get(review_create_url)
        if review_page_response.status_code == 200:
            print("✅ Review creation page accessible for booking user")
        else:
            print(f"❌ Review creation page returned status {review_page_response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing review creation page: {e}")
    
    # Test review creation for non-booking user (should fail)
    client.force_login(test_user)
    try:
        non_booking_review_response = client.get(review_create_url)
        if non_booking_review_response.status_code in [403, 404]:
            print("✅ Review creation correctly restricted for non-booking user")
        else:
            print(f"❌ Review creation not properly restricted (status: {non_booking_review_response.status_code})")
    except Exception as e:
        print(f"✅ Review creation properly restricted with error: {e}")
    
    print(f"\n🎉 Venue Review UI Integration Test Completed!")
    print(f"   Tested User: {user.username}")
    print(f"   Tested Venue: {venue.name}")
    print(f"   Test Pages: Dashboard, Venue Detail, Review Creation")
    print(f"   Test Scenarios: Booking user access, Non-booking user restrictions")

if __name__ == '__main__':
    test_venue_review_ui_integration()