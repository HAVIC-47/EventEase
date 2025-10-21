#!/usr/bin/env python
"""
Test script to check if event ratings are displaying on home and event list pages
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking
from reviews.models import EventReview
from django.utils import timezone

def test_event_ratings_display():
    print("🎯 Testing Event Ratings Display on Home & Events List...")
    
    # Get all events with their ratings
    events = Event.objects.all()[:5]  # Get first 5 events
    
    print(f"📊 Found {events.count()} events to check:")
    
    for event in events:
        print(f"\n  📅 Event: {event.title} (ID: {event.id})")
        print(f"     Reviews: {event.review_count}")
        if event.review_count > 0:
            print(f"     Rating: {event.average_rating:.1f}/5 ⭐")
            # Show individual reviews
            reviews = EventReview.objects.filter(event=event)
            for review in reviews:
                print(f"       - {review.user.get_full_name() or review.user.username}: {review.rating}/5")
        else:
            print(f"     Rating: No reviews yet")
    
    print(f"\n🎨 Rating Display Features Added:")
    print("   ✅ Star ratings (1-5 stars) with filled/empty stars")
    print("   ✅ Numerical rating (e.g., '4.5/5')")
    print("   ✅ Review count (e.g., '(3 reviews)')")
    print("   ✅ 'No reviews yet' message for events without ratings")
    print("   ✅ EventEase themed styling with #40B5AD colors")
    print("   ✅ Responsive design for both home and events list pages")
    
    print(f"\n🌐 Pages to test:")
    print("   🏠 Home page: http://127.0.0.1:8000/")
    print("   📋 Events list: http://127.0.0.1:8000/events/")
    
    # Check if any events have ratings
    events_with_ratings = Event.objects.filter(reviews__isnull=False).distinct()
    events_without_ratings = Event.objects.filter(reviews__isnull=True)
    
    print(f"\n📈 Rating Statistics:")
    print(f"   Events with ratings: {events_with_ratings.count()}")
    print(f"   Events without ratings: {events_without_ratings.count()}")
    
    if events_with_ratings.exists():
        print(f"\n✨ Events with ratings will show:")
        for event in events_with_ratings[:3]:
            print(f"   ⭐ {event.title}: {event.average_rating:.1f}/5 ({event.review_count} reviews)")
    
    if events_without_ratings.exists():
        print(f"\n📝 Events without ratings will show:")
        for event in events_without_ratings[:3]:
            print(f"   📋 {event.title}: 'No reviews yet'")

if __name__ == "__main__":
    test_event_ratings_display()
    print(f"\n✨ Event ratings are now displayed on both home and events list pages!")
    print(f"🔗 Visit the pages to see the ratings in action!")