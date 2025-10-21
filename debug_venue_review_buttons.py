#!/usr/bin/env python
"""
Debug venue detail view review button logic for specific venues.
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

def debug_venue_detail_review_logic():
    """
    Debug the venue detail view review button logic.
    """
    print("🔍 Debugging Venue Detail Review Button Logic...")
    print("=" * 60)
    
    # Test specific venue and user combinations that showed issues
    test_cases = [
        (2, 'Akhi_1'),  # UAP venue with Akhi_1 user
        (3, 'Akhi_1'),  # formula 1 venue with Akhi_1 user
        (4, 'eventmanager'),  # Test Convention Center with eventmanager
        (9, 'reviewer1'),  # Grand Ballroom with reviewer1
    ]
    
    for venue_id, username in test_cases:
        print(f"\n🎯 Testing Venue ID: {venue_id} with User: {username}")
        
        try:
            venue = Venue.objects.get(id=venue_id)
            user = User.objects.get(username=username)
            
            print(f"   🏢 Venue: {venue.name}")
            print(f"   👤 User: {user.username}")
            
            # Check bookings manually (same logic as venue detail view)
            completed_bookings = VenueBooking.objects.filter(
                user=user,
                venue=venue,
                status__in=['confirmed', 'completed'],
                end_date__lt=timezone.now()
            )
            
            print(f"   📊 Completed bookings count: {completed_bookings.count()}")
            
            if completed_bookings.exists():
                for booking in completed_bookings:
                    print(f"      - Booking {booking.id}: Status={booking.status}, End={booking.end_date}")
            
            user_has_booked = completed_bookings.exists()
            print(f"   ✅ User has booked venue: {user_has_booked}")
            
            # Check existing review
            user_venue_review = VenueReview.objects.filter(
                venue=venue,
                user=user
            ).first()
            
            print(f"   📝 User has existing review: {user_venue_review is not None}")
            if user_venue_review:
                print(f"      Review rating: {user_venue_review.rating}/5")
            
            # Calculate final result (same logic as venue detail view)
            user_can_review_venue = user_has_booked and not user_venue_review
            print(f"   🎯 user_can_review_venue: {user_can_review_venue}")
            
            # Test actual venue detail view
            client = Client()
            client.force_login(user)
            
            response = client.get(f'/venues/{venue_id}/')
            print(f"   📄 Venue detail status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check for review button text
                review_button_found = False
                button_types = [
                    ('Write a Review', 'add-review-btn'),
                    ('Write the First Review', 'add-review-btn'),
                    ('Edit Your Review', 'edit-review-btn'),
                    ('Add Review', 'any'),
                ]
                
                for button_text, button_class in button_types:
                    if button_text in content:
                        print(f"   ✅ Found button: '{button_text}'")
                        review_button_found = True
                        break
                
                if not review_button_found:
                    print(f"   ❌ No review button found in response")
                    
                    # Check if the user_can_review_venue variable is in the context
                    if 'user_can_review_venue' in content:
                        print(f"   📝 user_can_review_venue variable found in template")
                    else:
                        print(f"   ❌ user_can_review_venue variable NOT found in template")
                        
            else:
                print(f"   ❌ Venue detail view failed")
                
        except Venue.DoesNotExist:
            print(f"   ❌ Venue {venue_id} not found")
        except User.DoesNotExist:
            print(f"   ❌ User {username} not found")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 60)

if __name__ == '__main__':
    debug_venue_detail_review_logic()
