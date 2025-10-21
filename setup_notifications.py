#!/usr/bin/env python
import sqlite3
import os
from datetime import datetime

# Database path
db_path = "db.sqlite3"

def setup_complete_test_environment():
    """Setup a complete test environment with users and notifications"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Setting up test environment...")
        
        # Check if test user exists
        cursor.execute("SELECT id FROM auth_user WHERE username = 'testuser'")
        user = cursor.fetchone()
        
        if not user:
            # Create test user
            cursor.execute("""
                INSERT INTO auth_user (
                    username, email, first_name, last_name, 
                    is_active, is_staff, is_superuser, 
                    date_joined, password
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'testuser', 'test@example.com', 'Test', 'User',
                1, 0, 0, datetime.now().isoformat(),
                'pbkdf2_sha256$600000$testpass$hash'
            ))
            user_id = cursor.lastrowid
            print(f"✅ Created test user: testuser (ID: {user_id})")
        else:
            user_id = user[0]
            print(f"✅ Using existing user: testuser (ID: {user_id})")
        
        # Create admin user
        cursor.execute("SELECT id FROM auth_user WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            cursor.execute("""
                INSERT INTO auth_user (
                    username, email, first_name, last_name, 
                    is_active, is_staff, is_superuser, 
                    date_joined, password
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                'admin', 'admin@example.com', 'Admin', 'User',
                1, 1, 1, datetime.now().isoformat(),
                'pbkdf2_sha256$600000$admin123$hash'
            ))
            admin_id = cursor.lastrowid
            print(f"✅ Created admin user: admin (ID: {admin_id})")
        else:
            admin_id = admin[0]
            print(f"✅ Using existing admin: admin (ID: {admin_id})")
        
        # Clear existing notifications for clean testing
        cursor.execute("DELETE FROM core_notification WHERE user_id IN (?, ?)", (user_id, admin_id))
        
        # Create diverse test notifications
        notifications = [
            # For testuser
            (user_id, "Welcome to EventEase! 🎉", 
             "Thank you for joining our platform. Start exploring amazing events and venues!", 
             "booking_confirmation", "unread", 0),
            
            (user_id, "New Event: Summer Music Festival 🎵", 
             "A spectacular 3-day music festival featuring top artists is now available for booking.", 
             "event_booking", "unread", 0),
            
            (user_id, "Venue Booking Approved ✅", 
             "Great news! Your venue booking for 'Grand Conference Hall' has been approved.", 
             "venue_booking", "unread", 0),
            
            (user_id, "Event Reminder 📅", 
             "Your event 'Tech Conference 2025' starts tomorrow at 9:00 AM. Don't forget!", 
             "event_reminder", "unread", 0),
            
            (user_id, "Payment Successful 💳", 
             "Your payment of $150 for the event booking has been processed successfully.", 
             "booking_confirmation", "read", 1),
            
            # For admin
            (admin_id, "New User Registration 👤", 
             "A new user 'testuser' has registered on the platform.", 
             "event_booking", "unread", 0),
            
            (admin_id, "System Update Complete 🔧", 
             "The notification system has been successfully implemented and is working perfectly.", 
             "booking_confirmation", "unread", 0),
        ]
        
        # Insert notifications
        for notif in notifications:
            cursor.execute("""
                INSERT INTO core_notification (
                    user_id, title, message, notification_type, 
                    status, is_read, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (*notif, datetime.now().isoformat()))
        
        conn.commit()
        
        # Count notifications
        cursor.execute("SELECT COUNT(*) FROM core_notification WHERE user_id = ? AND is_read = 0", (user_id,))
        testuser_unread = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM core_notification WHERE user_id = ? AND is_read = 0", (admin_id,))
        admin_unread = cursor.fetchone()[0]
        
        print(f"\n📊 Notification Summary:")
        print(f"   📧 testuser: {testuser_unread} unread notifications")
        print(f"   📧 admin: {admin_unread} unread notifications")
        
        print(f"\n🔐 Login Credentials:")
        print(f"   👤 testuser / testpass123")
        print(f"   👤 admin / admin123")
        
        print(f"\n🌐 Test URLs:")
        print(f"   🏠 Home: http://127.0.0.1:8000/")
        print(f"   🔐 Login: http://127.0.0.1:8000/users/login/")
        print(f"   🔔 Notifications: http://127.0.0.1:8000/core/notifications/")
        
        print(f"\n✨ The notification bell should now show {testuser_unread} notifications when logged in as testuser!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    setup_complete_test_environment()
