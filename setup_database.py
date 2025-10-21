import sqlite3
import os
from datetime import datetime

# Database path
db_path = r"e:\event_ease_django - Copy_backup\db.sqlite3"

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_notification';")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Creating core_notification table...")
        
        # Create the table
        cursor.execute("""
            CREATE TABLE "core_notification" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "title" varchar(200) NOT NULL,
                "message" text NOT NULL,
                "notification_type" varchar(30) NOT NULL,
                "status" varchar(10) NOT NULL DEFAULT 'unread',
                "created_at" datetime NOT NULL,
                "event_id" integer,
                "venue_id" integer,
                "is_read" bool NOT NULL DEFAULT 0,
                "user_id" bigint NOT NULL,
                FOREIGN KEY (user_id) REFERENCES auth_user (id)
            );
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX core_notification_user_id ON core_notification (user_id);")
        cursor.execute("CREATE INDEX core_notification_created_at ON core_notification (created_at);")
        
        print("✅ Table created successfully!")
        
        # Mark migration as applied
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('core', '0001_initial', ?);
        """, (datetime.now().isoformat(),))
        
        print("✅ Migration marked as applied!")
        
    else:
        print("Table already exists!")
    
    # Create a test user if it doesn't exist
    cursor.execute("SELECT id FROM auth_user WHERE username = 'testuser';")
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("""
            INSERT INTO auth_user (username, email, first_name, last_name, is_active, is_staff, is_superuser, date_joined, password)
            VALUES ('testuser', 'test@example.com', 'Test', 'User', 1, 0, 0, ?, 'pbkdf2_sha256$600000$test$test');
        """, (datetime.now().isoformat(),))
        user_id = cursor.lastrowid
        print(f"✅ Created test user with ID: {user_id}")
    else:
        user_id = user[0]
        print(f"Using existing user with ID: {user_id}")
    
    # Create test notifications
    notifications = [
        ("Welcome to EventEase! 🎉", "Thank you for joining our platform. Start exploring amazing events!", "booking_confirmation"),
        ("New Event Available 🎵", "A spectacular music festival is now available for booking.", "event_booking"),
        ("Venue Booking Update 🏢", "Your venue booking request is being reviewed.", "venue_booking")
    ]
    
    for title, message, notif_type in notifications:
        cursor.execute("""
            INSERT OR IGNORE INTO core_notification (title, message, notification_type, status, created_at, is_read, user_id)
            VALUES (?, ?, ?, 'unread', ?, 0, ?);
        """, (title, message, notif_type, datetime.now().isoformat(), user_id))
    
    # Commit all changes
    conn.commit()
    
    # Count notifications
    cursor.execute("SELECT COUNT(*) FROM core_notification WHERE user_id = ?;", (user_id,))
    count = cursor.fetchone()[0]
    print(f"✅ Total notifications for testuser: {count}")
    
    print("\n🎉 Database setup complete!")
    print("You can now login with: testuser / testpass123")
    
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if conn:
        conn.close()
