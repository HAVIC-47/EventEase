#!/usr/bin/env python3
"""
Test script to verify comment images display in admin management
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth import get_user_model
from events.models import Event, EventComment
from venues.models import Venue, VenueComment
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse
import tempfile
from PIL import Image
import io

User = get_user_model()

def create_test_image():
    """Create a simple test image for comments"""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile('test_comment_image.jpg', img_io.read(), content_type='image/jpeg')

def test_comment_images_display():
    """Test the comment images display functionality"""
    print("🧪 Testing Comment Images Display in Admin Management")
    print("=" * 60)
    
    # Get or create test users
    admin_user, created = User.objects.get_or_create(
        username='admin_test',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: {admin_user.username}")
    else:
        print(f"📍 Using existing admin user: {admin_user.username}")
    
    regular_user, created = User.objects.get_or_create(
        username='regular_user_images',
        defaults={
            'email': 'regular_images@test.com',
            'first_name': 'Regular',
            'last_name': 'User'
        }
    )
    if created:
        regular_user.set_password('user123')
        regular_user.save()
        print(f"✅ Created regular user: {regular_user.username}")
    
    # Get or create test event
    from datetime import datetime
    event, created = Event.objects.get_or_create(
        title='Test Event with Images',
        defaults={
            'description': 'Test event for image comments',
            'organizer': admin_user,
            'start_date': datetime(2024, 2, 15, 10, 0),
            'end_date': datetime(2024, 2, 15, 18, 0),
            'venue_name': 'Test Venue',
            'venue_address': '123 Test Street',
            'contact_email': 'test@event.com',
            'max_attendees': 50
        }
    )
    if created:
        print(f"✅ Created test event: {event.title}")
    
    # Get or create test venue
    venue, created = Venue.objects.get_or_create(
        name='Test Venue for Images',
        defaults={
            'description': 'Test venue for image comments',
            'address': '123 Test Street',
            'owner': admin_user,
            'capacity': 100
        }
    )
    if created:
        print(f"✅ Created test venue: {venue.name}")
    
    # Create event comments with and without images
    print("\n📝 Creating event comments...")
    
    # Event comment with image
    test_image_1 = create_test_image()
    event_comment_with_image, created = EventComment.objects.get_or_create(
        event=event,
        user=regular_user,
        comment='This is a comment with an image attached!',
        defaults={'image': test_image_1}
    )
    if created:
        print(f"✅ Created event comment with image: ID {event_comment_with_image.id}")
        print(f"   📷 Image URL: {event_comment_with_image.image.url if event_comment_with_image.image else 'None'}")
    
    # Event comment without image
    event_comment_no_image, created = EventComment.objects.get_or_create(
        event=event,
        user=admin_user,
        comment='This is a regular comment without any image.',
        defaults={}
    )
    if created:
        print(f"✅ Created event comment without image: ID {event_comment_no_image.id}")
    
    # Create venue comments with and without images
    print("\n🏢 Creating venue comments...")
    
    # Venue comment with image
    test_image_2 = create_test_image()
    venue_comment_with_image, created = VenueComment.objects.get_or_create(
        venue=venue,
        user=regular_user,
        comment='Great venue! Here is a photo I took.',
        defaults={'image': test_image_2}
    )
    if created:
        print(f"✅ Created venue comment with image: ID {venue_comment_with_image.id}")
        print(f"   📷 Image URL: {venue_comment_with_image.image.url if venue_comment_with_image.image else 'None'}")
    
    # Venue comment without image
    venue_comment_no_image, created = VenueComment.objects.get_or_create(
        venue=venue,
        user=admin_user,
        comment='Nice venue, would recommend!',
        defaults={}
    )
    if created:
        print(f"✅ Created venue comment without image: ID {venue_comment_no_image.id}")
    
    # Test the admin comments management view
    print("\n🔍 Testing Admin Comments Management View...")
    
    from users.views import admin_comments_management
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/auth/admin/comments/')
    request.user = admin_user
    
    # Test the view
    try:
        response = admin_comments_management(request)
        print(f"✅ Admin comments management view responded with status: {response.status_code}")
        
        # Check if response contains our test comments
        content = response.content.decode('utf-8')
        
        # Check for comments with images
        has_image_indicators = content.count('📷 Has Image')
        print(f"📊 Found {has_image_indicators} comments with image indicators")
        
        # Check for image elements
        img_tags = content.count('<img src=')
        print(f"🖼️  Found {img_tags} image tags in the response")
        
        # Check for modal elements
        if 'imageModal' in content:
            print("✅ Image modal HTML found in response")
        else:
            print("❌ Image modal HTML not found")
            
        if 'openImageModal' in content:
            print("✅ JavaScript modal functions found in response")
        else:
            print("❌ JavaScript modal functions not found")
        
    except Exception as e:
        print(f"❌ Error testing view: {e}")
    
    # Display statistics
    print(f"\n📊 Comment Statistics:")
    print(f"   Total Event Comments: {EventComment.objects.count()}")
    print(f"   Event Comments with Images: {EventComment.objects.exclude(image='').count()}")
    print(f"   Total Venue Comments: {VenueComment.objects.count()}")
    print(f"   Venue Comments with Images: {VenueComment.objects.exclude(image='').count()}")
    
    # URLs for testing
    print(f"\n🌐 URLs for Manual Testing:")
    print(f"   Admin Dashboard: http://127.0.0.1:8000/auth/admin/dashboard/")
    print(f"   Comments Management: http://127.0.0.1:8000/auth/admin/comments/")
    print(f"   Event Detail: http://127.0.0.1:8000/events/{event.id}/")
    print(f"   Venue Detail: http://127.0.0.1:8000/venues/{venue.id}/")
    
    print(f"\n✅ Comment Images Display Test Complete!")
    print(f"📝 Next Steps:")
    print(f"   1. Start Django server: python manage.py runserver")
    print(f"   2. Login as admin: {admin_user.username} / admin123")
    print(f"   3. Visit Comments Management page")
    print(f"   4. Look for thumbnail images in comments")
    print(f"   5. Click images to open in modal view")

if __name__ == '__main__':
    test_comment_images_display()