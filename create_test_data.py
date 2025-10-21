#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from venues.models import Venue, VenueBooking
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

def create_test_data():
    # Create venue manager user
    try:
        venue_manager = User.objects.get(username='venuemanager')
        print("Venue manager already exists")
    except User.DoesNotExist:
        venue_manager = User.objects.create_user(
            username='venuemanager',
            email='manager@venue.com',
            password='testpass123',
            first_name='John',
            last_name='Manager'
        )
        try:
            UserProfile.objects.create(
                user=venue_manager,
                role='venue_manager',
                phone='123-456-7890'
            )
        except:
            # Profile might already exist, update it
            profile, created = UserProfile.objects.get_or_create(
                user=venue_manager,
                defaults={
                    'role': 'venue_manager',
                    'phone': '123-456-7890'
                }
            )
        print("Created venue manager: venuemanager / testpass123")

    # Create event manager user
    try:
        event_manager = User.objects.get(username='eventmanager')
        print("Event manager already exists")
    except User.DoesNotExist:
        event_manager = User.objects.create_user(
            username='eventmanager',
            email='event@manager.com',
            password='testpass123',
            first_name='Jane',
            last_name='EventPlanner'
        )
        try:
            UserProfile.objects.create(
                user=event_manager,
                role='event_manager',
                phone='123-456-7891'
            )
        except:
            # Profile might already exist, update it
            profile, created = UserProfile.objects.get_or_create(
                user=event_manager,
                defaults={
                    'role': 'event_manager',
                    'phone': '123-456-7891'
                }
            )
        print("Created event manager: eventmanager / testpass123")

    # Create a test venue
    try:
        venue = Venue.objects.get(name='Test Convention Center')
        print("Test venue already exists")
    except Venue.DoesNotExist:
        venue = Venue.objects.create(
            name='Test Convention Center',
            description='A beautiful venue for events and conferences',
            venue_type='conference_hall',
            manager=venue_manager,
            address='123 Main Street',
            city='Sample City',
            state='Sample State',
            zipcode='12345',
            capacity=500,
            price_per_hour=Decimal('150.00'),
            price_per_day=Decimal('1000.00'),
            contact_email='manager@venue.com',
            contact_phone='123-456-7890',
            has_parking=True,
            has_wifi=True,
            has_catering=True,
            has_av_equipment=True,
            has_air_conditioning=True,
        )
        print("Created test venue: Test Convention Center")

    # Create some test bookings
    try:
        booking = VenueBooking.objects.get(event_title='Wedding Reception')
        print("Test booking already exists")
    except VenueBooking.DoesNotExist:
        start_date = timezone.now() + timedelta(days=30)
        end_date = start_date + timedelta(hours=6)
        
        booking = VenueBooking.objects.create(
            venue=venue,
            user=event_manager,
            event_title='Wedding Reception',
            event_description='Beautiful wedding reception for 200 guests',
            start_date=start_date,
            end_date=end_date,
            contact_email='event@manager.com',
            contact_phone='123-456-7891',
            special_requirements='Need white table linens and centerpieces',
            total_amount=Decimal('900.00'),
            status='pending'
        )
        print("Created test booking: Wedding Reception")

    # Create another booking
    try:
        booking2 = VenueBooking.objects.get(event_title='Corporate Conference')
        print("Second test booking already exists")
    except VenueBooking.DoesNotExist:
        start_date2 = timezone.now() + timedelta(days=15)
        end_date2 = start_date2 + timedelta(hours=8)
        
        booking2 = VenueBooking.objects.create(
            venue=venue,
            user=event_manager,
            event_title='Corporate Conference',
            event_description='Annual company conference with presentations',
            start_date=start_date2,
            end_date=end_date2,
            contact_email='event@manager.com',
            contact_phone='123-456-7891',
            special_requirements='Need projector and microphone system',
            total_amount=Decimal('1200.00'),
            status='confirmed'
        )
        print("Created second test booking: Corporate Conference")

    print("\n=== Test Data Summary ===")
    print(f"Venue Manager: venuemanager / testpass123")
    print(f"Event Manager: eventmanager / testpass123")
    print(f"Venue: {venue.name}")
    print(f"Bookings: {VenueBooking.objects.filter(venue=venue).count()}")
    print("\nYou can now test the booking management system!")

if __name__ == '__main__':
    create_test_data()
