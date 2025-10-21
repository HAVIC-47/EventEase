# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('notification_type', models.CharField(choices=[('event_booking', 'Event Booking'), ('venue_booking', 'Venue Booking'), ('booking_confirmation', 'Booking Confirmation'), ('event_reminder', 'Event Reminder'), ('payment_success', 'Payment Success'), ('venue_booking_request', 'Venue Booking Request'), ('event_registration', 'Event Registration')], max_length=30)),
                ('status', models.CharField(choices=[('unread', 'Unread'), ('read', 'Read')], default='unread', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event_id', models.PositiveIntegerField(blank=True, null=True)),
                ('venue_id', models.PositiveIntegerField(blank=True, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
