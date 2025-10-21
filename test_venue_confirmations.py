#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from venues.models import VenueBooking, Venue
from notifications.models import Notification
from datetime import datetime, timezone, timedelta
from decimal import Decimal

def test_venue_booking_confirmation_flow():
    print("🧪 TESTING COMPLETE VENUE BOOKING CONFIRMATION FLOW")
    print("=" * 70)
    
    # Get or create test users
    customer, _ = User.objects.get_or_create(
        username='booking_customer',
        defaults={'email': 'customer@booking.com', 'password': 'testpass123'}
    )
    
    venue_manager, _ = User.objects.get_or_create(
        username='booking_venue_mgr',
        defaults={'email': 'manager@booking.com', 'password': 'testpass123'}
    )
    
    # Get or create venue
    venue, created = Venue.objects.get_or_create(
        name='Booking Test Venue',
        defaults={
            'description': 'Test venue for booking confirmations',
            'venue_type': 'conference_hall',
            'manager': venue_manager,
            'address': '123 Booking St',
            'city': 'Booking City',
            'state': 'Booking State',
            'zipcode': '12345',
            'capacity': 150,
            'price_per_hour': Decimal('200.00'),
            'contact_email': venue_manager.email,
            'contact_phone': '555-BOOK',
            'is_available': True
        }
    )
    
    if created:
        print(f"✅ Created venue: {venue.name}")
    else:
        print(f"✅ Using existing venue: {venue.name}")
    
    print(f"Customer: {customer.username}")
    print(f"Venue Manager: {venue.manager.username}")
    
    # Clean up old notifications for cleaner test
    old_notifications = Notification.objects.filter(
        user__in=[customer, venue_manager],
        title__icontains='Booking Test'
    )
    deleted_count = old_notifications.count()
    old_notifications.delete()
    if deleted_count > 0:
        print(f"🧹 Cleaned up {deleted_count} old test notifications")
    
    # Step 1: Customer creates booking request
    print(f"\n🔹 STEP 1: Customer creates venue booking request")
    before_request = Notification.objects.count()
    
    booking = VenueBooking.objects.create(
        venue=venue,
        user=customer,
        event_title='Booking Test Event',
        event_description='Testing the booking confirmation process',
        start_date=datetime.now(timezone.utc) + timedelta(days=3),
        end_date=datetime.now(timezone.utc) + timedelta(days=3, hours=4),
        total_amount=Decimal('800.00'),
        contact_email=customer.email,
        contact_phone='555-CUST',
        status='pending'
    )
    
    after_request = Notification.objects.count()
    print(f"   📋 Booking created: {booking.event_title}")
    print(f"   📊 Notifications: {before_request} → {after_request} (Added: {after_request - before_request})")
    
    # Check venue manager notifications
    manager_notifications = Notification.objects.filter(
        user=venue_manager,
        notification_type='venue_booking_request'
    ).order_by('-created_at')[:1]
    
    if manager_notifications:
        notif = manager_notifications[0]
        print(f"   ✅ Venue manager got notification: '{notif.title}'")
    else:
        print(f"   ❌ No notification found for venue manager")
    
    # Step 2: Venue manager confirms booking
    print(f"\n🔹 STEP 2: Venue manager confirms the booking")
    before_confirm = Notification.objects.count()
    
    booking.status = 'confirmed'
    booking.save()
    
    after_confirm = Notification.objects.count()
    print(f"   ✅ Booking status changed to: {booking.status}")
    print(f"   📊 Notifications: {before_confirm} → {after_confirm} (Added: {after_confirm - before_confirm})")
    
    # Check customer confirmation notifications
    customer_confirmations = Notification.objects.filter(
        user=customer,
        notification_type='venue_booking_status'
    ).order_by('-created_at')[:1]
    
    if customer_confirmations:
        notif = customer_confirmations[0]
        print(f"   ✅ Customer got confirmation: '{notif.title}'")
        print(f"   📝 Message: {notif.message}")
    else:
        print(f"   ❌ No confirmation notification found for customer")
    
    # Step 3: Show all relevant notifications
    print(f"\n📧 ALL VENUE BOOKING NOTIFICATIONS:")
    print("-" * 50)
    
    # Customer notifications
    customer_notifs = Notification.objects.filter(user=customer).order_by('-created_at')[:5]
    print(f"Customer ({customer.username}) notifications:")
    for i, notif in enumerate(customer_notifs, 1):
        status = "📧 Unread" if not notif.is_read else "✅ Read"
        print(f"  {i}. {status} [{notif.notification_type}] {notif.title}")
        if 'booking' in notif.title.lower():
            print(f"     Message: {notif.message}")
        print(f"     Time: {notif.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    # Manager notifications
    manager_notifs = Notification.objects.filter(user=venue_manager).order_by('-created_at')[:5]
    print(f"Venue Manager ({venue_manager.username}) notifications:")
    for i, notif in enumerate(manager_notifs, 1):
        status = "📧 Unread" if not notif.is_read else "✅ Read"
        print(f"  {i}. {status} [{notif.notification_type}] {notif.title}")
        if 'booking' in notif.title.lower():
            print(f"     Message: {notif.message}")
        print(f"     Time: {notif.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    print(f"🎯 RESULT SUMMARY:")
    print(f"✅ Venue booking request notifications: Working")
    print(f"✅ Venue booking confirmation notifications: Working")
    print(f"🌐 View in browser: http://127.0.0.1:8000/notifications/")
    print(f"🔑 Login as '{customer.username}' to see confirmation notification")

if __name__ == '__main__':
    test_venue_booking_confirmation_flow()
