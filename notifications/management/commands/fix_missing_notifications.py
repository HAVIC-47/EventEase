"""
Management command to fix missing venue booking confirmation notifications
"""
from django.core.management.base import BaseCommand
from venues.models import VenueBooking
from notifications.models import Notification


class Command(BaseCommand):
    help = 'Fix missing venue booking confirmation notifications'

    def handle(self, *args, **options):
        self.stdout.write("=== Fixing Missing Venue Booking Confirmations ===")
        
        # Find all confirmed bookings
        confirmed_bookings = VenueBooking.objects.filter(status='confirmed')
        fixed_count = 0
        
        for booking in confirmed_bookings:
            # Check if confirmation notification exists
            existing_confirmation = Notification.objects.filter(
                user=booking.user,
                message__icontains=f'booking for "{booking.venue.name}" has been confirmed',
                notification_type='venue_booking_status'
            ).exists()
            
            if not existing_confirmation:
                # Create the missing confirmation notification
                Notification.objects.create(
                    user=booking.user,
                    title="Venue Booking Confirmed",
                    message=f'Your venue booking for "{booking.venue.name}" has been confirmed.',
                    notification_type='venue_booking_status',
                    venue_id=booking.venue.id,
                    booking_id=booking.id
                )
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Fixed: {booking.user.username} - {booking.venue.name} (Booking #{booking.id})"
                    )
                )
        
        if fixed_count == 0:
            self.stdout.write(self.style.SUCCESS("✅ All venue booking confirmations are already present!"))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Fixed {fixed_count} missing venue booking confirmation notifications")
            )
