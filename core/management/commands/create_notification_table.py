from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create the notification table manually'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='core_notification';
            """)
            
            if cursor.fetchone():
                self.stdout.write(self.style.WARNING('Table core_notification already exists!'))
                return
            
            # Create the table
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
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX "core_notification_user_id_4d844a38" 
                ON "core_notification" ("user_id");
            """)
            
            cursor.execute("""
                CREATE INDEX "core_notification_created_at_7b477b49" 
                ON "core_notification" ("created_at");
            """)
            
            # Mark migration as applied
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied)
                VALUES ('core', '0001_initial', datetime('now'));
            """)
            
        self.stdout.write(self.style.SUCCESS('Successfully created notification table!'))
