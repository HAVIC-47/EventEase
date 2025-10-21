#!/usr/bin/env python
"""
Test script to create a sample booking and verify the counts update
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking, TicketCategory, BookingTicketItem

def create_test_booking():
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing test user: {user.username}")
    
    # Get event 8
    try:
        event = Event.objects.get(pk=8)
        print(f"Event: {event.title}")
        
        # Get ticket categories
        categories = list(event.ticket_categories.all())
        if not categories:
            print("No ticket categories found!")
            return
        
        # Create a booking
        booking = EventBooking.objects.create(
            event=event,
            user=user,
            attendee_name=f"{user.first_name} {user.last_name}",
            attendee_email=user.email,
            attendee_phone="+1234567890",
            status='confirmed',
            amount=0
        )
        print(f"Created booking: {booking.id}")
        
        # Add some ticket items
        total_amount = 0
        total_quantity = 0
        
        # Buy 2 student tickets
        student_category = categories[0]  # Assuming first is student
        ticket_item1 = BookingTicketItem.objects.create(
            booking=booking,
            ticket_category=student_category,
            quantity=2,
            price_per_ticket=student_category.price
        )
        total_amount += ticket_item1.subtotal
        total_quantity += ticket_item1.quantity
        print(f"Added {ticket_item1.quantity} x {student_category.name} tickets")
        
        # Buy 1 premium ticket
        if len(categories) > 2:
            premium_category = categories[2]  # Assuming third is premium
            ticket_item2 = BookingTicketItem.objects.create(
                booking=booking,
                ticket_category=premium_category,
                quantity=1,
                price_per_ticket=premium_category.price
            )
            total_amount += ticket_item2.subtotal
            total_quantity += ticket_item2.quantity
            print(f"Added {ticket_item2.quantity} x {premium_category.name} tickets")
        
        # Update booking totals
        booking.amount = total_amount
        booking.total_amount = total_amount
        booking.attendees_count = total_quantity
        booking.save()
        
        print(f"Updated booking - Total amount: ${total_amount}, Total tickets: {total_quantity}")
        
        # Check updated counts
        print("\nUpdated Ticket Categories:")
        for category in event.ticket_categories.all():
            print(f"  {category.name}:")
            print(f"    Total available: {category.quantity_available}")
            print(f"    Tickets sold: {category.tickets_sold}")
            print(f"    Tickets available: {category.tickets_available}")
        
        # Calculate total tickets sold
        total_tickets_sold = sum(cat.tickets_sold for cat in event.ticket_categories.all())
        print(f"\nTotal tickets sold across all categories: {total_tickets_sold}")
        print(f"Remaining capacity: {event.max_attendees - total_tickets_sold}")
        
    except Event.DoesNotExist:
        print("Event with ID 8 not found")

if __name__ == "__main__":
    create_test_booking()
