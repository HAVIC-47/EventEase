#!/usr/bin/env python
"""
Demo script to showcase the venue comment like functionality
"""

import os
import django

# Setup Django first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from venues.models import Venue, VenueComment, VenueCommentLike

def demo_like_functionality():
    """Demonstrate the like functionality with visual output"""
    print("🌟 VENUE COMMENT LIKE SYSTEM DEMO")
    print("=" * 50)
    
    # Get test data
    venue = Venue.objects.first()
    users = User.objects.all()[:4]
    
    if not venue or len(users) < 2:
        print("❌ Insufficient test data")
        return
        
    print(f"🏢 Venue: {venue.name}")
    print(f"👥 Users: {', '.join([u.username for u in users])}")
    
    # Create a demo comment
    demo_user = users[0]
    comment, created = VenueComment.objects.get_or_create(
        venue=venue,
        user=demo_user,
        defaults={
            'comment': '🎉 This venue is absolutely amazing! Perfect for our upcoming event. The facilities are top-notch and the staff is very professional.'
        }
    )
    
    print(f"\n💬 Demo Comment (by {demo_user.username}):")
    print(f"   '{comment.comment[:80]}...'")
    print(f"   📝 Comment ID: {comment.id}")
    
    # Clear existing likes for demo
    VenueCommentLike.objects.filter(comment=comment).delete()
    
    print(f"\n📊 Initial State:")
    print(f"   ❤️  Like count: {comment.like_count}")
    print(f"   👤 Users who liked: None")
    
    # Demo like interactions
    print(f"\n🎬 Like Interactions Demo:")
    
    liked_users = []
    for i, user in enumerate(users, 1):
        result = comment.toggle_like(user)
        if result:
            liked_users.append(user.username)
            action = "❤️  LIKED"
        else:
            if user.username in liked_users:
                liked_users.remove(user.username)
            action = "💔 UNLIKED"
            
        print(f"   Step {i}: {user.username} -> {action}")
        print(f"           Like count: {comment.like_count}")
        print(f"           Users who liked: {', '.join(liked_users) if liked_users else 'None'}")
        print()
    
    # Show final state
    print(f"🏁 Final State:")
    print(f"   ❤️  Total likes: {comment.like_count}")
    print(f"   👥 Liked by: {', '.join([like.user.username for like in comment.likes.all()])}")
    
    # Template filter demo
    print(f"\n🔧 Template Filter Demo:")
    from venues.templatetags.venue_extras import is_liked_by
    
    for user in users:
        liked = is_liked_by(comment, user)
        status = "❤️  LIKES" if liked else "🤍 DOESN'T LIKE"
        print(f"   {user.username}: {status} this comment")
    
    # AJAX endpoint demo
    print(f"\n🌐 AJAX Endpoint Demo:")
    from django.urls import reverse
    
    try:
        url = reverse('venues:comment_like_toggle', kwargs={'comment_id': comment.id})
        print(f"   📡 AJAX URL: {url}")
        print(f"   📝 Usage: POST request to toggle like/unlike")
        print(f"   📤 Response: JSON with success, is_liked, like_count, message")
    except Exception as e:
        print(f"   ❌ URL configuration error: {e}")
    
    # Database model features
    print(f"\n🏗️  Database Features:")
    print(f"   🔒 Unique constraint: One like per user per comment")
    print(f"   🔄 Toggle method: comment.toggle_like(user)")
    print(f"   📊 Like count property: comment.like_count")
    print(f"   ✅ User check method: comment.is_liked_by_user(user)")
    
    print(f"\n🎉 Demo Complete!")
    print(f"📝 Comment ID {comment.id} now has {comment.like_count} likes")
    print(f"🌐 Visit http://127.0.0.1:8000/venues/{venue.id}/ to see it in action!")

if __name__ == "__main__":
    demo_like_functionality()