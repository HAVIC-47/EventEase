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

def show_current_notifications():
    print("🔔 CURRENT VENUE BOOKING CONFIRMATION NOTIFICATIONS")
    print("=" * 70)
    
    # Show all venue booking status notifications
    venue_confirmations = Notification.objects.filter(
        notification_type='venue_booking_status'
    ).order_by('-created_at')
    
    print(f"📊 Total venue booking status notifications: {venue_confirmations.count()}")
    print()
    
    if venue_confirmations:
        print("📋 ALL VENUE BOOKING CONFIRMATION NOTIFICATIONS:")
        print("-" * 50)
        
        for i, notif in enumerate(venue_confirmations, 1):
            status = "📧 Unread" if not notif.is_read else "✅ Read"
            print(f"{i}. {status} User: {notif.user.username}")
            print(f"   Title: {notif.title}")
            print(f"   Message: {notif.message}")
            print(f"   Created: {notif.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Type: {notif.notification_type}")
            print()
    
    # Show users who should have notifications
    users_with_venue_notifs = User.objects.filter(
        user_notifications__notification_type='venue_booking_status'
    ).distinct()
    
    print(f"👥 USERS WITH VENUE BOOKING NOTIFICATIONS:")
    print("-" * 40)
    
    for user in users_with_venue_notifs:
        user_notifs = Notification.objects.filter(
            user=user,
            notification_type='venue_booking_status'
        ).order_by('-created_at')
        
        print(f"🔐 {user.username} (Password: testpass123)")
        print(f"   📧 Venue notifications: {user_notifs.count()}")
        
        # Show latest notification
        if user_notifs:
            latest = user_notifs.first()
            status = "📧 Unread" if not latest.is_read else "✅ Read"
            print(f"   Latest: {status} '{latest.title}'")
            print(f"   Message: {latest.message}")
        print()
    
    print("🌐 TO VIEW NOTIFICATIONS:")
    print("-" * 25)
    print("1. Go to: http://127.0.0.1:8000/admin/")
    print("   Login: admin / admin")
    print("   Check: notifications > Notifications")
    print()
    print("2. Go to: http://127.0.0.1:8000/notifications/")
    print("   Login with any username above + password: testpass123")
    print()
    
    # Test with fresh_customer specifically
    fresh_customer = User.objects.filter(username='fresh_customer').first()
    if fresh_customer:
        fresh_notifs = Notification.objects.filter(user=fresh_customer).order_by('-created_at')
        print(f"🎯 FRESH CUSTOMER TEST RESULTS:")
        print("-" * 30)
        print(f"Username: fresh_customer")
        print(f"Total notifications: {fresh_notifs.count()}")
        
        for notif in fresh_notifs:
            status = "📧 Unread" if not notif.is_read else "✅ Read"
            print(f"  {status} [{notif.notification_type}] {notif.title}")
            print(f"    {notif.message}")

if __name__ == '__main__':
    show_current_notifications()
