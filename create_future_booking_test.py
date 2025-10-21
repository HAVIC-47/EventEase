#!/usr/bin/env python
"""
Create test data for future venue bookings to test review waiting functionality.
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

def create_future_venue_booking():
    """
    Create a future venue booking to test the waiting functionality.
    """
    print("🎯 Creating Future Venue Booking for Testing...")
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='future_booking_user',
        defaults={
            'email': 'future@test.com',
            'first_name': 'Future',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created user: {user.username}")
    else:
        print(f"✅ Using existing user: {user.username}")
    
    # Get a venue
    venue = Venue.objects.first()
    if not venue:
        print("❌ No venues found in database")
        return
    
    print(f"✅ Using venue: {venue.name}")
    
    # Create a future booking
    future_date = timezone.now() + timedelta(days=7)  # 7 days in the future
    end_date = future_date + timedelta(hours=4)
    
    booking, created = VenueBooking.objects.get_or_create(
        user=user,
        venue=venue,
        event_title='Future Test Event',
        defaults={
            'event_description': 'A future event to test review waiting functionality',
            'start_date': future_date,
            'end_date': end_date,
            'total_amount': 500.00,
            'status': 'confirmed',
            'contact_email': user.email,
            'contact_phone': '555-TEST',
            'special_requirements': 'Testing future booking review functionality'
        }
    )
    
    if created:
        print(f"✅ Created future booking:")
        print(f"   Event: {booking.event_title}")
        print(f"   Start: {booking.start_date}")
        print(f"   End: {booking.end_date}")
        print(f"   Status: {booking.status}")
        print(f"   User can access dashboard at: http://127.0.0.1:8000/auth/dashboard/")
        print(f"   Login with username: {user.username}, password: testpass123")
    else:
        print(f"✅ Future booking already exists:")
        print(f"   Event: {booking.event_title}")
        print(f"   End Date: {booking.end_date}")
    
    # Check if booking is in the future
    now = timezone.now()
    print(f"\n📅 Current time: {now}")
    print(f"📅 Booking end time: {booking.end_date}")
    print(f"✅ Booking is in future: {booking.end_date > now}")
    
    print(f"\n🎉 Future venue booking setup complete!")
    print(f"💡 Now you can test the 'Please wait for the event to end' functionality")

if __name__ == '__main__':
    create_future_venue_booking()