import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Notification

# Get or create a user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
)

if created:
    user.set_password('testpass123')
    user.save()
    print(f"Created user: {user.username}")
else:
    print(f"Using existing user: {user.username}")

# Create a test notification
notification = Notification.objects.create(
    user=user,
    title="Test Notification",
    message="This is a test notification to verify the system is working.",
    notification_type='booking_confirmation'
)

print(f"Created notification: {notification.title}")
print(f"Unread count for {user.username}: {Notification.objects.filter(user=user, is_read=False).count()}")
