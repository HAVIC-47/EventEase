#!/usr/bin/env python
"""
Complete notification system setup
"""
import os
import django
import sqlite3
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User

def complete_setup():
    """Complete setup of notification system"""
    print("🚀 Setting up notification system...")
    
    # Connect to SQLite database
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Ensure the core_notification table exists
        cursor.execute("DROP TABLE IF EXISTS core_notification;")
        
        create_table_sql = """
        CREATE TABLE "core_notification" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "title" varchar(200) NOT NULL,
            "message" text NOT NULL,
            "notification_type" varchar(30) NOT NULL DEFAULT 'system',
            "is_read" boolean NOT NULL DEFAULT 0,
            "created_at" datetime NOT NULL,
            "updated_at" datetime NOT NULL,
            "event_id" integer,
            "venue_id" integer,
            "booking_id" integer,
            "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
        );
        """
        
        cursor.execute(create_table_sql)
        
        # Create indexes
        cursor.execute('CREATE INDEX "core_notification_user_id_3d727c5c" ON "core_notification" ("user_id");')
        cursor.execute('CREATE INDEX "core_notification_user_id_created_at_idx" ON "core_notification" ("user_id", "created_at");')
        cursor.execute('CREATE INDEX "core_notification_user_id_is_read_idx" ON "core_notification" ("user_id", "is_read");')
        
        conn.commit()
        print("✅ Created core_notification table with indexes")
        
        # 2. Update migration record
        cursor.execute("DELETE FROM django_migrations WHERE app = 'core' AND name = '0001_initial';")
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('core', '0001_initial', datetime('now'))
        """)
        conn.commit()
        print("✅ Updated migration record")
        
        # 3. Create test users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@eventease.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print(f"✅ Created admin user: admin / admin123")
        else:
            print(f"✅ Admin user already exists: admin")
        
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@eventease.com',
                'first_name': 'Test',
                'last_name': 'User',
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            print(f"✅ Created test user: testuser / testpass123")
        else:
            print(f"✅ Test user already exists: testuser")
        
        # 4. Create sample notifications directly in database
        now = datetime.now().isoformat()
        
        # Clear existing notifications
        cursor.execute("DELETE FROM core_notification;")
        
        # Sample notifications for test user
        notifications = [
            (test_user.id, 'Welcome to EventEase!', 'Thank you for joining EventEase. Start exploring amazing events near you.', 'system', 0, now, now),
            (test_user.id, 'New Event Available', 'A new music concert has been added to your area. Check it out!', 'event_registration', 0, now, now),
            (test_user.id, 'Event Reminder', 'Don\'t forget! Your booked event "Tech Conference 2025" is tomorrow.', 'event_reminder', 0, now, now),
            (test_user.id, 'Booking Confirmed', 'Your booking for "Art Exhibition" has been confirmed. Booking ID: #12345', 'booking_confirmation', 1, now, now),
            (test_user.id, 'Payment Successful', 'Your payment of $50.00 for "Cooking Workshop" has been processed successfully.', 'payment_success', 1, now, now),
            (admin_user.id, 'System Update Complete', 'EventEase system has been updated to version 2.1. Check the changelog for new features.', 'system', 0, now, now),
            (admin_user.id, 'New User Registration', 'A new user has registered on the platform.', 'system', 0, now, now),
        ]
        
        cursor.executemany("""
            INSERT INTO core_notification 
            (user_id, title, message, notification_type, is_read, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, notifications)
        
        conn.commit()
        print(f"✅ Created {len(notifications)} sample notifications")
        
        print("\n🎉 Notification system setup completed!")
        print("\nLogin credentials:")
        print("👤 Admin: admin / admin123")
        print("👤 Test User: testuser / testpass123")
        print("\nTest URLs:")
        print("🏠 Home: http://127.0.0.1:8000/")
        print("🔐 Login: http://127.0.0.1:8000/users/login/")
        print("🔔 Notifications: http://127.0.0.1:8000/core/notifications/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    complete_setup()
