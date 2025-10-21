#!/usr/bin/env python
"""
Script to fix the notifications database issue
"""
import os
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.db import connection

def create_notification_table():
    """Create the core_notification table directly in SQLite"""
    
    # Connect to SQLite database
    db_path = 'db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_notification';")
    if cursor.fetchone():
        print("✅ core_notification table already exists")
        conn.close()
        return
    
    # Create the table
    create_table_sql = """
    CREATE TABLE "core_notification" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "title" varchar(200) NOT NULL,
        "message" text NOT NULL,
        "notification_type" varchar(30) NOT NULL,
        "status" varchar(10) NOT NULL,
        "created_at" datetime NOT NULL,
        "event_id" integer,
        "venue_id" integer,
        "booking_id" integer,
        "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
    );
    """
    
    try:
        cursor.execute(create_table_sql)
        
        # Create index for user_id
        cursor.execute('CREATE INDEX "core_notification_user_id_idx" ON "core_notification" ("user_id");')
        
        # Create index for created_at for ordering
        cursor.execute('CREATE INDEX "core_notification_created_at_idx" ON "core_notification" ("created_at");')
        
        conn.commit()
        print("✅ Successfully created core_notification table")
        
        # Mark migration as applied
        cursor.execute("""
            INSERT OR IGNORE INTO django_migrations (app, name, applied) 
            VALUES ('core', '0001_initial', datetime('now'))
        """)
        conn.commit()
        print("✅ Marked migration as applied")
        
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_notification_table()
    print("🎉 Database fix completed!")
