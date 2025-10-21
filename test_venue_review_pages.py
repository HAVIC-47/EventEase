#!/usr/bin/env python
"""
Test venue review pages to ensure they load without errors after the fix.
"""

import os
import sys
import django
from django.test import Client

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from venues.models import Venue
from reviews.models import VenueReview

def test_venue_review_pages():
    """
    Test all venue review pages to ensure they load correctly.
    """
    print("🔍 Testing Venue Review Pages After Fix...")
    print("=" * 60)
    
    # Get all venues that have reviews
    venues_with_reviews = []
    for venue in Venue.objects.all():
        review_count = VenueReview.objects.filter(venue=venue).count()
        if review_count > 0:
            venues_with_reviews.append((venue, review_count))
    
    print(f"Found {len(venues_with_reviews)} venues with reviews")
    print()
    
    client = Client()
    
    for venue, review_count in venues_with_reviews:
        print(f"🏢 Testing Venue: {venue.name} (ID: {venue.id})")
        print(f"   Reviews: {review_count}")
        
        try:
            # Test venue reviews page
            response = client.get(f'/reviews/venue/{venue.id}/')
            
            if response.status_code == 200:
                print(f"   ✅ Venue reviews page loads successfully")
                
                # Check if the page contains review data
                content = response.content.decode('utf-8')
                if 'reviews' in content.lower() or 'rating' in content.lower():
                    print(f"   ✅ Page contains review content")
                else:
                    print(f"   ⚠️ Page loads but may not contain review content")
                    
            else:
                print(f"   ❌ Venue reviews page failed: Status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error loading venue reviews page: {e}")
        
        print("-" * 40)
    
    # Test a venue without reviews to ensure it doesn't crash
    print("\n🏢 Testing Venue Without Reviews...")
    venues_without_reviews = Venue.objects.exclude(
        id__in=[v.id for v, _ in venues_with_reviews]
    ).first()
    
    if venues_without_reviews:
        try:
            response = client.get(f'/reviews/venue/{venues_without_reviews.id}/')
            if response.status_code == 200:
                print(f"   ✅ Venue without reviews page loads successfully")
            else:
                print(f"   ❌ Venue without reviews page failed: Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error loading venue without reviews page: {e}")
    else:
        print("   ℹ️ All venues have reviews - no venue without reviews to test")
    
    print(f"\n🎉 Venue Review Pages Test Complete!")

if __name__ == '__main__':
    test_venue_review_pages()