#!/usr/bin/env python
import os
import sys
import django
import sqlite3

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.conf import settings

def create_notification_table():
    """Create the notification table directly in SQLite"""
    db_path = settings.DATABASES['default']['NAME']
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='core_notification';
        """)
        
        if cursor.fetchone():
            print("core_notification table already exists!")
            return
        
        # Create the core_notification table
        cursor.execute("""
            CREATE TABLE "core_notification" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "title" varchar(200) NOT NULL,
                "message" text NOT NULL,
                "notification_type" varchar(30) NOT NULL,
                "status" varchar(10) NOT NULL,
                "created_at" datetime NOT NULL,
                "event_id" integer,
                "venue_id" integer,
                "is_read" bool NOT NULL,
                "user_id" bigint NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        """)
        
        # Create index on user_id for performance
        cursor.execute("""
            CREATE INDEX "core_notification_user_id_4d844a38" 
            ON "core_notification" ("user_id");
        """)
        
        # Create index on created_at for ordering
        cursor.execute("""
            CREATE INDEX "core_notification_created_at_7b477b49" 
            ON "core_notification" ("created_at");
        """)
        
        # Commit changes
        conn.commit()
        
        print("✅ Successfully created core_notification table!")
        
        # Mark migration as applied in django_migrations table
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('core', '0001_initial', datetime('now'));
        """)
        
        conn.commit()
        print("✅ Migration marked as applied!")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_notification_table()
