import os
import django
import sys

# Add the project directory to Python path
sys.path.append(r'E:\Event easy\event_ease_django - version-12')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventComment
from venues.models import Venue, VenueComment
from django.utils import timezone

def test_comments_management():
    """Test the comments management functionality"""
    
    print("💬 Testing Comments Management System")
    print("=" * 60)
    
    # Get total comments count
    total_event_comments = EventComment.objects.count()
    total_venue_comments = VenueComment.objects.count()
    total_comments = total_event_comments + total_venue_comments
    
    print("📊 COMMENTS OVERVIEW:")
    print(f"   📅 Event Comments: {total_event_comments}")
    print(f"   🏢 Venue Comments: {total_venue_comments}")
    print(f"   💬 Total Comments: {total_comments}")
    
    print("\n" + "=" * 60)
    
    # Test event comments
    print("📅 EVENT COMMENTS ANALYSIS:")
    event_comments = EventComment.objects.select_related('user', 'event').order_by('-created_at')[:10]
    
    if event_comments:
        print(f"   📋 Recent Event Comments (Top {event_comments.count()}):")
        for i, comment in enumerate(event_comments, 1):
            is_reply = "↳ Reply" if comment.parent else "💬 Main"
            has_image = "📷" if comment.image else "📝"
            print(f"      {i}. [{is_reply}] {has_image} \"{comment.event.title}\"")
            print(f"         👤 By: {comment.user.get_full_name() or comment.user.username}")
            print(f"         💭 Comment: {comment.comment[:100]}{'...' if len(comment.comment) > 100 else ''}")
            print(f"         📅 Date: {comment.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
    else:
        print("   📭 No event comments found.")
    
    print("\n" + "=" * 60)
    
    # Test venue comments  
    print("🏢 VENUE COMMENTS ANALYSIS:")
    venue_comments = VenueComment.objects.select_related('user', 'venue').order_by('-created_at')[:10]
    
    if venue_comments:
        print(f"   📋 Recent Venue Comments (Top {venue_comments.count()}):")
        for i, comment in enumerate(venue_comments, 1):
            is_reply = "↳ Reply" if comment.parent else "💬 Main"
            has_image = "📷" if comment.image else "📝"
            print(f"      {i}. [{is_reply}] {has_image} \"{comment.venue.name}\"")
            print(f"         👤 By: {comment.user.get_full_name() or comment.user.username}")
            print(f"         💭 Comment: {comment.comment[:100]}{'...' if len(comment.comment) > 100 else ''}")
            print(f"         📅 Date: {comment.created_at.strftime('%Y-%m-%d %H:%M')}")
            print()
    else:
        print("   📭 No venue comments found.")
    
    print("\n" + "=" * 60)
    
    # Test combined comments (as would appear in management page)
    print("🔄 COMBINED COMMENTS SIMULATION:")
    
    all_comments = []
    
    # Add event comments
    for comment in EventComment.objects.select_related('user', 'event').all():
        all_comments.append({
            'id': comment.id,
            'type': 'event',
            'content_name': comment.event.title,
            'user': comment.user,
            'comment': comment.comment,
            'created_at': comment.created_at,
            'has_image': bool(comment.image),
            'is_reply': comment.parent is not None,
        })
    
    # Add venue comments
    for comment in VenueComment.objects.select_related('user', 'venue').all():
        all_comments.append({
            'id': comment.id,
            'type': 'venue',
            'content_name': comment.venue.name,
            'user': comment.user,
            'comment': comment.comment,
            'created_at': comment.created_at,
            'has_image': bool(comment.image),
            'is_reply': comment.parent is not None,
        })
    
    # Sort by creation date
    all_comments.sort(key=lambda x: x['created_at'], reverse=True)
    
    print(f"   📋 All Comments (Combined, Top 15):")
    for i, comment in enumerate(all_comments[:15], 1):
        type_icon = "📅" if comment['type'] == 'event' else "🏢"
        reply_icon = "↳" if comment['is_reply'] else "💬"
        image_icon = "📷" if comment['has_image'] else "📝"
        
        print(f"      {i}. {reply_icon} {type_icon} {image_icon} \"{comment['content_name']}\"")
        print(f"         👤 {comment['user'].get_full_name() or comment['user'].username}")
        print(f"         💭 {comment['comment'][:80]}{'...' if len(comment['comment']) > 80 else ''}")
        print(f"         📅 {comment['created_at'].strftime('%Y-%m-%d %H:%M')} ({comment['type'].title()})")
        print()
    
    print("\n" + "=" * 60)
    
    # Test user activity
    print("👥 USER COMMENT ACTIVITY:")
    users_with_comments = User.objects.annotate(
        event_comment_count=django.db.models.Count('event_comments'),
        venue_comment_count=django.db.models.Count('venue_comments')
    ).filter(
        django.db.models.Q(event_comment_count__gt=0) | 
        django.db.models.Q(venue_comment_count__gt=0)
    ).order_by('-event_comment_count', '-venue_comment_count')
    
    print(f"   📋 Most Active Commenters:")
    for i, user in enumerate(users_with_comments[:10], 1):
        total_user_comments = user.event_comment_count + user.venue_comment_count
        print(f"      {i}. {user.get_full_name() or user.username}")
        print(f"         📅 Event Comments: {user.event_comment_count}")
        print(f"         🏢 Venue Comments: {user.venue_comment_count}")
        print(f"         💬 Total: {total_user_comments}")
        print()
    
    print("\n" + "=" * 60)
    
    # Test content with most comments
    print("🎯 MOST COMMENTED CONTENT:")
    
    # Events with most comments
    events_with_comments = Event.objects.annotate(
        comment_count=django.db.models.Count('comments')
    ).filter(comment_count__gt=0).order_by('-comment_count')[:5]
    
    print("   📅 Most Commented Events:")
    for i, event in enumerate(events_with_comments, 1):
        print(f"      {i}. \"{event.title}\" - {event.comment_count} comments")
        print(f"         👤 By: {event.organizer.get_full_name() or event.organizer.username}")
    
    # Venues with most comments
    venues_with_comments = Venue.objects.annotate(
        comment_count=django.db.models.Count('comments')
    ).filter(comment_count__gt=0).order_by('-comment_count')[:5]
    
    print("\n   🏢 Most Commented Venues:")
    for i, venue in enumerate(venues_with_comments, 1):
        print(f"      {i}. \"{venue.name}\" - {venue.comment_count} comments")
        print(f"         👤 By: {venue.manager.get_full_name() or venue.manager.username}")
    
    print("\n" + "=" * 60)
    print("✅ Comments Management System Test Complete!")
    print("🌐 Access Comments Management at: http://127.0.0.1:8000/auth/admin/comments/")
    print("🚀 Admin Dashboard: http://127.0.0.1:8000/auth/admin/dashboard/")
    
    return True

if __name__ == "__main__":
    # Import django.db.models for aggregation
    import django.db.models
    test_comments_management()