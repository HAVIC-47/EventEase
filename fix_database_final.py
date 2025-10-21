#!/usr/bin/env python
"""
Direct database setup script for notifications
"""
import os
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

def setup_database():
    """Setup the database directly"""
    
    # Connect to SQLite database
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Drop the table if it exists (fresh start)
        cursor.execute("DROP TABLE IF EXISTS core_notification;")
        
        # Create the core_notification table matching our model
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
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX "core_notification_user_id_3d727c5c" ON "core_notification" ("user_id");')
        cursor.execute('CREATE INDEX "core_notification_user_id_created_at_idx" ON "core_notification" ("user_id", "created_at");')
        cursor.execute('CREATE INDEX "core_notification_user_id_is_read_idx" ON "core_notification" ("user_id", "is_read");')
        
        conn.commit()
        print("✅ Successfully created core_notification table with indexes")
        
        # Update or insert migration record
        cursor.execute("DELETE FROM django_migrations WHERE app = 'core' AND name = '0001_initial';")
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('core', '0001_initial', datetime('now'))
        """)
        conn.commit()
        print("✅ Updated migration record")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
    print("🎉 Database setup completed!")
