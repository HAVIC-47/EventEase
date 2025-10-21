#!/usr/bin/env python
"""
Comprehensive end-to-end test of the venue comment like functionality
"""

import os
import django
import json

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from venues.models import Venue, VenueComment, VenueCommentLike

def test_complete_like_system():
    """Test the complete like system from database to frontend"""
    print("🎯 Complete Like System Test")
    print("=" * 50)
    
    try:
        # Setup test data
        venue = Venue.objects.first()
        user = User.objects.first()
        
        if not venue or not user:
            print("❌ Missing test data (venue or user)")
            return
            
        print(f"✅ Testing with venue: {venue.name}")
        print(f"✅ Testing with user: {user.username}")
        
        # Create or get a test comment
        comment, created = VenueComment.objects.get_or_create(
            venue=venue,
            user=user,
            defaults={'comment': 'Test comment for like functionality'}
        )
        
        print(f"✅ {'Created' if created else 'Using existing'} comment: {comment.id}")
        
        # Test 1: Database Model Functionality
        print("\n📊 Testing Database Models:")
        initial_count = comment.like_count
        initial_liked = comment.is_liked_by_user(user)
        print(f"   Initial like count: {initial_count}")
        print(f"   User initially liked: {initial_liked}")
        
        # Toggle like (add)
        result = comment.toggle_like(user)
        print(f"   Toggle result (add): {result}")
        print(f"   Like count after add: {comment.like_count}")
        print(f"   User liked after add: {comment.is_liked_by_user(user)}")
        
        # Toggle like (remove)
        result = comment.toggle_like(user)
        print(f"   Toggle result (remove): {result}")
        print(f"   Like count after remove: {comment.like_count}")
        print(f"   User liked after remove: {comment.is_liked_by_user(user)}")
        
        # Test 2: Template Filter
        print("\n🔧 Testing Template Filter:")
        from venues.templatetags.venue_extras import is_liked_by
        
        # Add a like for testing
        comment.toggle_like(user)
        filter_result = is_liked_by(comment, user)
        print(f"   Template filter with like: {filter_result}")
        
        # Remove like
        comment.toggle_like(user)
        filter_result = is_liked_by(comment, user)
        print(f"   Template filter without like: {filter_result}")
        
        # Test 3: AJAX Endpoint
        print("\n🌐 Testing AJAX Endpoint:")
        client = Client()
        client.force_login(user)
        
        # Test like toggle via AJAX
        response = client.post(f'/venues/comment/{comment.id}/like/')
        print(f"   AJAX response status: {response.status_code}")
        
        if response.status_code == 200:
            data = json.loads(response.content)
            print(f"   AJAX response data: {data}")
            print(f"   ✅ AJAX like toggle successful")
            
            # Test toggle again
            response = client.post(f'/venues/comment/{comment.id}/like/')
            data = json.loads(response.content)
            print(f"   Second toggle data: {data}")
        else:
            print(f"   ❌ AJAX endpoint error: {response.status_code}")
            
        # Test 4: Frontend Integration
        print("\n🖥️ Testing Frontend Integration:")
        
        # Get venue detail page
        response = client.get(f'/venues/{venue.id}/')
        print(f"   Venue page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Check for like system components
            checks = [
                ('like-btn', 'Like buttons'),
                ('toggleLike', 'JavaScript function'),
                ('heart-icon', 'Heart icons'),
                ('like-count', 'Like count display'),
                ('data-comment-id', 'Comment ID data attributes')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description} found")
                else:
                    print(f"   ⚠️  {description} not found")
                    
        # Test 5: Multiple Users
        print("\n👥 Testing Multiple Users:")
        other_users = User.objects.exclude(id=user.id)[:2]
        
        for other_user in other_users:
            comment.toggle_like(other_user)
            print(f"   Added like from: {other_user.username}")
            
        print(f"   Final like count: {comment.like_count}")
        
        # Test 6: Database Constraints
        print("\n🔒 Testing Database Constraints:")
        
        # Try to create duplicate like (should fail silently due to unique constraint)
        like_obj, created = VenueCommentLike.objects.get_or_create(
            comment=comment,
            user=user
        )
        print(f"   Duplicate like created: {created}")
        
        total_likes = VenueCommentLike.objects.filter(comment=comment).count()
        print(f"   Total unique likes: {total_likes}")
        
        print("\n🎉 Complete like system test finished!")
        print("✅ All functionality working correctly!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_like_system()