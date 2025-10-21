#!/usr/bin/env python3
"""
Simple test script to verify comment images functionality
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.models import EventComment
from venues.models import VenueComment

def test_comment_images_simple():
    """Simple test to check existing comments and images"""
    print("🧪 Testing Comment Images Display - Simple Check")
    print("=" * 50)
    
    # Check existing comments
    event_comments = EventComment.objects.all()
    venue_comments = VenueComment.objects.all()
    
    print(f"📊 Current Database State:")
    print(f"   Total Event Comments: {event_comments.count()}")
    print(f"   Event Comments with Images: {event_comments.exclude(image='').count()}")
    print(f"   Total Venue Comments: {venue_comments.count()}")
    print(f"   Venue Comments with Images: {venue_comments.exclude(image='').count()}")
    
    # Test if we have any comments with images
    event_comments_with_images = event_comments.exclude(image='')
    venue_comments_with_images = venue_comments.exclude(image='')
    
    if event_comments_with_images.exists():
        print(f"\n📸 Event Comments with Images:")
        for comment in event_comments_with_images[:3]:  # Show first 3
            print(f"   - ID: {comment.id}, Event: {comment.event.title}")
            print(f"     Image: {comment.image.url if comment.image else 'None'}")
            print(f"     Comment: {comment.comment[:50]}...")
    
    if venue_comments_with_images.exists():
        print(f"\n🏢 Venue Comments with Images:")
        for comment in venue_comments_with_images[:3]:  # Show first 3
            print(f"   - ID: {comment.id}, Venue: {comment.venue.name}")
            print(f"     Image: {comment.image.url if comment.image else 'None'}")
            print(f"     Comment: {comment.comment[:50]}...")
    
    # Test the view logic (without HTTP request)
    print(f"\n🔍 Testing View Data Structure:")
    
    # Simulate the view logic
    all_comments = []
    
    for comment in event_comments.order_by('-created_at')[:5]:
        all_comments.append({
            'id': comment.id,
            'type': 'event',
            'content_name': comment.event.title,
            'content_id': comment.event.id,
            'user': comment.user,
            'comment': comment.comment,
            'created_at': comment.created_at,
            'has_image': bool(comment.image),
            'image': comment.image,
            'image_url': comment.image.url if comment.image else None,
        })
    
    for comment in venue_comments.order_by('-created_at')[:5]:
        all_comments.append({
            'id': comment.id,
            'type': 'venue',
            'content_name': comment.venue.name,
            'content_id': comment.venue.id,
            'user': comment.user,
            'comment': comment.comment,
            'created_at': comment.created_at,
            'has_image': bool(comment.image),
            'image': comment.image,
            'image_url': comment.image.url if comment.image else None,
        })
    
    print(f"   Total comments in test structure: {len(all_comments)}")
    comments_with_images = [c for c in all_comments if c['has_image']]
    print(f"   Comments with images: {len(comments_with_images)}")
    
    for comment in comments_with_images[:2]:  # Show first 2
        print(f"   - {comment['type'].title()} Comment: {comment['content_name']}")
        print(f"     Has image: {comment['has_image']}")
        print(f"     Image URL: {comment['image_url']}")
    
    print(f"\n✅ Simple Test Complete!")
    print(f"🌐 URLs for Manual Testing:")
    print(f"   Admin Dashboard: http://127.0.0.1:8000/auth/admin/dashboard/")
    print(f"   Comments Management: http://127.0.0.1:8000/auth/admin/comments/")
    
    if comments_with_images:
        print(f"\n🎯 Expected Behavior:")
        print(f"   1. Images should display as thumbnails in the comment column")
        print(f"   2. Clicking images should open them in a modal")
        print(f"   3. Modal should have close button and escape key support")
    else:
        print(f"\n⚠️  No comments with images found!")
        print(f"   Create some comments with images to test the functionality")

if __name__ == '__main__':
    test_comment_images_simple()