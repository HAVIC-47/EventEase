#!/usr/bin/env python
"""
Quick script to create a test event with categories
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append('e:/event_ease_django - Copy_backup')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.models import Event, TicketCategory
from users.models import User

# Get the first superuser or create one
user = User.objects.filter(is_superuser=True).first()
if not user:
    user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

# Create event
start_date = datetime.now() + timedelta(days=15)
end_date = start_date + timedelta(hours=2)

event = Event.objects.create(
    title="Concert with Multiple Tickets",
    description="Test event with different ticket categories",
    event_type="conference",
    venue_name="Test Venue",
    venue_address="123 Test Street",
    start_date=start_date,
    end_date=end_date,
    max_attendees=300,
    ticket_price=40.00,
    is_free=False,
    organizer=user,
    contact_email="test@example.com",
    is_active=True
)

# Create categories
TicketCategory.objects.create(
    event=event,
    name="General Admission",
    category_type="general",
    price=35.00,
    quantity_available=150,
    description="Standard entry ticket"
)

TicketCategory.objects.create(
    event=event,
    name="VIP Package",
    category_type="vip",
    price=75.00,
    quantity_available=50,
    description="VIP access with premium benefits"
)

TicketCategory.objects.create(
    event=event,
    name="Student Discount",
    category_type="student",
    price=20.00,
    quantity_available=100,
    description="Discounted tickets for students"
)

print(f"Created event: {event.title} (ID: {event.id})")
print(f"URL: http://127.0.0.1:8000/events/{event.id}/")
print("Categories:")
for cat in event.ticket_categories.all():
    print(f"  - {cat.name}: ${cat.price}")
