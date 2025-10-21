#!/usr/bin/env python
"""
Test confirmed venue bookings review functionality in dashboard.
"""

import os
import sys
import django
from datetime import datetime, timedelta
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

def test_confirmed_venue_review_functionality():
    """
    Test the confirmed venue bookings review functionality.
    """
    print("🏢 Testing Confirmed Venue Bookings Review Functionality...")
    print("=" * 70)
    
    # Get confirmed venue bookings
    confirmed_bookings = VenueBooking.objects.filter(status='confirmed').order_by('end_date')
    
    print(f"Found {confirmed_bookings.count()} confirmed venue bookings")
    print()
    
    client = Client()
    now = timezone.now()
    
    # Test different scenarios
    past_completed_bookings = []
    future_bookings = []
    
    for booking in confirmed_bookings:
        if booking.end_date < now:
            past_completed_bookings.append(booking)
        else:
            future_bookings.append(booking)
    
    print(f"📊 Booking Status:")
    print(f"   Past completed bookings: {len(past_completed_bookings)}")
    print(f"   Future bookings: {len(future_bookings)}")
    print()
    
    # Test past completed bookings (should allow reviews)
    print("🔍 Testing Past Completed Bookings (Should Allow Reviews):")
    for booking in past_completed_bookings[:3]:  # Test first 3
        user = booking.user
        venue = booking.venue
        
        print(f"   🎯 User: {user.username} | Venue: {venue.name}")
        print(f"      End Date: {booking.end_date}")
        print(f"      Booking Completed: {booking.end_date < now}")
        
        # Check if user has existing review
        existing_review = VenueReview.objects.filter(venue=venue, user=user).first()
        print(f"      Has Existing Review: {existing_review is not None}")
        
        # Login and test dashboard
        client.force_login(user)
        dashboard_response = client.get('/auth/dashboard/')
        
        if dashboard_response.status_code == 200:
            dashboard_content = dashboard_response.content.decode('utf-8')
            
            # Check if venue appears in confirmed section
            if venue.name in dashboard_content:
                print(f"      ✅ Venue appears in dashboard")
                
                # Check review status messages
                if existing_review:
                    if 'You have reviewed this venue' in dashboard_content:
                        print(f"      ✅ Shows 'You have reviewed this venue' status")
                    if 'Update Review' in dashboard_content:
                        print(f"      ✅ Shows 'Update Review' button")
                else:
                    if 'You can review this venue' in dashboard_content:
                        print(f"      ✅ Shows 'You can review this venue' status")
                    if 'Leave Review' in dashboard_content:
                        print(f"      ✅ Shows 'Leave Review' button")
            else:
                print(f"      ❌ Venue not found in dashboard")
        else:
            print(f"      ❌ Dashboard failed to load")
        
        print("-" * 50)
    
    # Test future bookings (should show wait message)
    print("\n🔍 Testing Future Bookings (Should Show Wait Message):")
    for booking in future_bookings[:2]:  # Test first 2
        user = booking.user
        venue = booking.venue
        
        print(f"   🎯 User: {user.username} | Venue: {venue.name}")
        print(f"      End Date: {booking.end_date}")
        print(f"      Booking Completed: {booking.end_date < now}")
        
        # Login and test dashboard
        client.force_login(user)
        dashboard_response = client.get('/auth/dashboard/')
        
        if dashboard_response.status_code == 200:
            dashboard_content = dashboard_response.content.decode('utf-8')
            
            if venue.name in dashboard_content:
                print(f"      ✅ Venue appears in dashboard")
                
                # Check for wait message
                if 'Please wait for the event to end' in dashboard_content:
                    print(f"      ✅ Shows 'Please wait for the event to end' message")
                
                # Check that review button is disabled
                if 'disabled' in dashboard_content and 'Review' in dashboard_content:
                    print(f"      ✅ Review button is disabled")
                else:
                    print(f"      ⚠️ Review button status unclear")
            else:
                print(f"      ❌ Venue not found in dashboard")
        else:
            print(f"      ❌ Dashboard failed to load")
        
        print("-" * 50)
    
    print(f"\n🎉 Confirmed Venue Review Functionality Test Complete!")

if __name__ == '__main__':
    test_confirmed_venue_review_functionality()