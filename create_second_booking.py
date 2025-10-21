#!/usr/bin/env python
"""
Create another test booking to see the numbers update
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking, TicketCategory, BookingTicketItem

def create_second_booking():
    # Get or create another test user
    user, created = User.objects.get_or_create(
        username='testuser2',
        defaults={
            'email': 'test2@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing test user: {user.username}")
    
    # Get event 8
    event = Event.objects.get(pk=8)
    print(f"Event: {event.title}")
    
    # Get ticket categories
    categories = list(event.ticket_categories.all())
    
    # Create a second booking
    booking = EventBooking.objects.create(
        event=event,
        user=user,
        attendee_name=f"{user.first_name} {user.last_name}",
        attendee_email=user.email,
        attendee_phone="+1234567891",
        status='confirmed',
        amount=0
    )
    print(f"Created second booking: {booking.id}")
    
    # Add different ticket combinations
    total_amount = 0
    total_quantity = 0
    
    # Buy 1 VIP ticket and 2 basic tickets
    vip_category = categories[3]  # VIP
    basic_category = categories[1]  # basic
    
    # VIP ticket
    ticket_item1 = BookingTicketItem.objects.create(
        booking=booking,
        ticket_category=vip_category,
        quantity=1,
        price_per_ticket=vip_category.price
    )
    total_amount += ticket_item1.subtotal
    total_quantity += ticket_item1.quantity
    print(f"Added {ticket_item1.quantity} x {vip_category.name} tickets")
    
    # Basic tickets
    ticket_item2 = BookingTicketItem.objects.create(
        booking=booking,
        ticket_category=basic_category,
        quantity=2,
        price_per_ticket=basic_category.price
    )
    total_amount += ticket_item2.subtotal
    total_quantity += ticket_item2.quantity
    print(f"Added {ticket_item2.quantity} x {basic_category.name} tickets")
    
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

if __name__ == "__main__":
    create_second_booking()
