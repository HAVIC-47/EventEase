#!/usr/bin/env python
"""
Test script to verify booking counts update correctly
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking, TicketCategory, BookingTicketItem

def test_booking_counts():
    # Get event 8
    try:
        event = Event.objects.get(pk=8)
        print(f"Event: {event.title}")
        print(f"Max attendees: {event.max_attendees}")
        
        # Check current bookings
        confirmed_bookings = EventBooking.objects.filter(
            event=event, 
            status__in=['confirmed', 'paid']
        )
        print(f"Current bookings: {confirmed_bookings.count()}")
        
        # Check ticket categories
        print("\nTicket Categories:")
        for category in event.ticket_categories.all():
            print(f"  {category.name}:")
            print(f"    Total available: {category.quantity_available}")
            print(f"    Tickets sold: {category.tickets_sold}")
            print(f"    Tickets available: {category.tickets_available}")
        
        # Calculate total tickets sold across all categories
        total_tickets_sold = 0
        for booking in confirmed_bookings:
            ticket_items = BookingTicketItem.objects.filter(booking=booking)
            for item in ticket_items:
                total_tickets_sold += item.quantity
                print(f"    Booking {booking.id}: {item.quantity} x {item.ticket_category.name}")
        
        print(f"\nTotal tickets sold across all categories: {total_tickets_sold}")
        print(f"Remaining capacity: {event.max_attendees - total_tickets_sold}")
        
    except Event.DoesNotExist:
        print("Event with ID 8 not found")

if __name__ == "__main__":
    test_booking_counts()
