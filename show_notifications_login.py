#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from notifications.models import Notification

def show_login_instructions():
    print("🔑 LOGIN INSTRUCTIONS TO SEE VENUE BOOKING CONFIRMATIONS")
    print("=" * 70)
    
    # Find users with venue booking status notifications
    users_with_confirmations = User.objects.filter(
        user_notifications__notification_type='venue_booking_status'
    ).distinct()
    
    print("👥 Users who have venue booking confirmation notifications:")
    print("-" * 50)
    
    for user in users_with_confirmations:
        venue_notifications = Notification.objects.filter(
            user=user,
            notification_type='venue_booking_status'
        ).order_by('-created_at')
        
        unread_count = venue_notifications.filter(is_read=False).count()
        total_count = venue_notifications.count()
        
        print(f"🔐 Username: {user.username}")
        print(f"   Password: testpass123")
        print(f"   📧 Venue confirmations: {total_count} total ({unread_count} unread)")
        
        # Show latest notifications
        for notif in venue_notifications[:2]:
            status = "📧 Unread" if not notif.is_read else "✅ Read"
            print(f"   {status} {notif.title}")
            print(f"      Message: {notif.message}")
            print(f"      Time: {notif.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    print("🌐 TO SEE THE NOTIFICATIONS:")
    print("-" * 30)
    print("1. Go to: http://127.0.0.1:8000/notifications/")
    print("2. Login with any of the usernames above + password: testpass123")
    print("3. You will see venue booking confirmation notifications!")
    print()
    
    print("🎯 QUICK TEST:")
    print("-" * 15)
    print("Login as 'booking_customer' to see the latest venue confirmation!")

if __name__ == '__main__':
    show_login_instructions()
