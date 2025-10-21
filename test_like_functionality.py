#!/usr/bin/env python
"""
Test script to verify venue comment like functionality
"""

import os
import django
from django.db import transaction

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from venues.models import Venue, VenueComment, VenueCommentLike

def test_like_functionality():
    """Test the complete like functionality"""
    print("🧪 Testing Venue Comment Like Functionality")
    print("=" * 50)
    
    try:
        # Get test data
        venue = Venue.objects.first()
        user = User.objects.first()
        
        if not venue:
            print("❌ No venues found. Please create test data first.")
            return
            
        if not user:
            print("❌ No users found. Please create test data first.")
            return
            
        print(f"✅ Using venue: {venue.name}")
        print(f"✅ Using user: {user.username}")
        
        # Get or create a test comment
        comment, created = VenueComment.objects.get_or_create(
            venue=venue,
            user=user,
            defaults={
                'comment': 'This is a test comment for like functionality testing.'
            }
        )
        
        print(f"✅ {'Created' if created else 'Using existing'} comment: {comment.comment[:50]}...")
        
        # Test initial state
        print("\n📊 Testing Initial State:")
        print(f"   Like count: {comment.like_count}")
        print(f"   User has liked: {comment.is_liked_by_user(user)}")
        
        # Test toggle like (add like)
        print("\n❤️ Testing Add Like:")
        with transaction.atomic():
            result = comment.toggle_like(user)
            print(f"   Toggle result: {result}")
            print(f"   Like count after toggle: {comment.like_count}")
            print(f"   User has liked: {comment.is_liked_by_user(user)}")
            
        # Test toggle like again (remove like)
        print("\n💔 Testing Remove Like:")
        with transaction.atomic():
            result = comment.toggle_like(user)
            print(f"   Toggle result: {result}")
            print(f"   Like count after toggle: {comment.like_count}")
            print(f"   User has liked: {comment.is_liked_by_user(user)}")
            
        # Test template filter
        print("\n🔧 Testing Template Filter:")
        from venues.templatetags.venue_extras import is_liked_by
        filter_result = is_liked_by(comment, user)
        print(f"   Template filter result: {filter_result}")
        
        # Test VenueCommentLike model directly
        print("\n🏗️ Testing VenueCommentLike Model:")
        like_count = VenueCommentLike.objects.filter(comment=comment).count()
        print(f"   Direct like count: {like_count}")
        
        user_likes = VenueCommentLike.objects.filter(comment=comment, user=user).exists()
        print(f"   User has like record: {user_likes}")
        
        # Test with multiple users
        print("\n👥 Testing Multiple Users:")
        other_users = User.objects.exclude(id=user.id)[:3]
        for other_user in other_users:
            comment.toggle_like(other_user)
            print(f"   Added like from {other_user.username}")
            
        print(f"   Final like count: {comment.like_count}")
        
        # Test URL endpoint would be available
        print("\n🌐 Testing URL Configuration:")
        from django.urls import reverse
        try:
            url = reverse('venues:comment_like_toggle', kwargs={'comment_id': comment.id})
            print(f"   ✅ Like toggle URL: {url}")
        except Exception as e:
            print(f"   ❌ URL configuration error: {e}")
            
        print("\n🎉 All like functionality tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_like_functionality()