#!/usr/bin/env python
"""
Create a test event with ticket categories for testing
"""
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.models import Event, TicketCategory
from users.models import User
from venues.models import Venue

def create_test_event_with_categories():
    """Create a test event with multiple ticket categories"""
    
    print("Creating test event with ticket categories...")
    
    # Get or create an event manager user
    try:
        event_manager = User.objects.filter(profile__role='event_manager').first()
        if not event_manager:
            event_manager = User.objects.filter(is_superuser=True).first()
            if not event_manager:
                print("No suitable user found. Creating one...")
                event_manager = User.objects.create_user(
                    username='event_manager_test',
                    email='manager@test.com',
                    password='testpass123',
                    first_name='Event',
                    last_name='Manager'
                )
                # Create profile if needed
                if hasattr(event_manager, 'profile'):
                    event_manager.profile.role = 'event_manager'
                    event_manager.profile.save()
    except Exception as e:
        print(f"Error getting user: {e}")
        return
    
    # Create or get venue
    venue, created = Venue.objects.get_or_create(
        name="Test Concert Hall",
        defaults={
            'address': '123 Music Street, Concert City',
            'capacity': 500,
            'description': 'A beautiful concert hall for events',
            'contact_email': 'venue@test.com'
        }
    )
    
    # Create event
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(hours=3)
    
    event = Event.objects.create(
        title="Multi-Category Concert Event",
        description="A fantastic concert with multiple ticket categories to choose from!",
        event_type="conference",
        venue=venue,
        venue_name=venue.name,
        venue_address=venue.address,
        start_date=start_date,
        end_date=end_date,
        max_attendees=500,
        ticket_price=50.00,  # Default price if no categories
        is_free=False,
        organizer=event_manager,
        contact_email="concert@test.com",
        is_active=True
    )
    
    # Create multiple ticket categories
    categories = [
        {
            'name': 'General Admission',
            'category_type': 'general',
            'price': 35.00,
            'quantity_available': 200,
            'description': 'Standard seating with great views'
        },
        {
            'name': 'VIP Experience',
            'category_type': 'vip',
            'price': 85.00,
            'quantity_available': 50,
            'description': 'Premium seating with complimentary drinks and exclusive access'
        },
        {
            'name': 'Student Discount',
            'category_type': 'student',
            'price': 25.00,
            'quantity_available': 75,
            'description': 'Discounted tickets for students (ID required at venue)'
        },
        {
            'name': 'Early Bird Special',
            'category_type': 'early_bird',
            'price': 30.00,
            'quantity_available': 100,
            'description': 'Limited time early bird pricing - save $5!'
        }
    ]
    
    for cat_data in categories:
        TicketCategory.objects.create(
            event=event,
            **cat_data
        )
    
    print(f"✅ Created event: {event.title} (ID: {event.id})")
    print(f"   URL: http://127.0.0.1:8000/events/{event.id}/")
    print(f"   Categories created: {len(categories)}")
    
    for cat in event.ticket_categories.all():
        print(f"   - {cat.name}: ${cat.price} ({cat.tickets_available} available)")
    
    return event

if __name__ == "__main__":
    event = create_test_event_with_categories()
