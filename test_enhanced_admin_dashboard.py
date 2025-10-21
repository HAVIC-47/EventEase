import os
import django
import sys

# Add the project directory to Python path
sys.path.append(r'E:\Event easy\event_ease_django - version-12')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, EventBooking, EventComment
from venues.models import Venue, VenueBooking, VenueComment
from reviews.models import EventReview, VenueReview
from django.db.models import Count, Avg
from django.utils import timezone

def test_admin_dashboard_data():
    """Test the data collection for enhanced admin dashboard"""
    
    print("🚀 Testing Enhanced Admin Dashboard Data Collection")
    print("=" * 60)
    
    # Test basic counts
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_venues = Venue.objects.count()
    total_event_reviews = EventReview.objects.count()
    total_venue_reviews = VenueReview.objects.count()
    total_event_comments = EventComment.objects.count()
    total_venue_comments = VenueComment.objects.count()
    total_event_bookings = EventBooking.objects.count()
    total_venue_bookings = VenueBooking.objects.count()
    
    print("📊 PLATFORM STATISTICS:")
    print(f"   👥 Total Users: {total_users}")
    print(f"   📅 Total Events: {total_events}")
    print(f"   🏢 Total Venues: {total_venues}")
    print(f"   ⭐ Total Reviews: {total_event_reviews + total_venue_reviews} (Events: {total_event_reviews}, Venues: {total_venue_reviews})")
    print(f"   💬 Total Comments: {total_event_comments + total_venue_comments} (Events: {total_event_comments}, Venues: {total_venue_comments})")
    print(f"   🎫 Total Bookings: {total_event_bookings + total_venue_bookings} (Events: {total_event_bookings}, Venues: {total_venue_bookings})")
    
    print("\n" + "=" * 60)
    
    # Test user statistics with activity
    print("👥 USER ACTIVITY ANALYSIS:")
    users_with_stats = User.objects.select_related('profile').annotate(
        # Event statistics
        events_posted=Count('organized_events', distinct=True),
        event_bookings_received=Count('organized_events__bookings', distinct=True),
        
        # Venue statistics
        venues_posted=Count('managed_venues', distinct=True),
        venue_bookings_received=Count('managed_venues__bookings', distinct=True),
        
        # Review statistics
        event_reviews_given=Count('event_reviews', distinct=True),
        venue_reviews_given=Count('venue_reviews', distinct=True),
        
        # Comment statistics
        event_comments_posted=Count('event_comments', distinct=True),
        venue_comments_posted=Count('venue_comments', distinct=True),
        
        # Booking statistics as customer
        event_bookings_made=Count('event_bookings', distinct=True),
        venue_bookings_made=Count('venue_bookings', distinct=True)
    ).order_by('-date_joined')[:10]
    
    print(f"   📋 Analyzing top {users_with_stats.count()} users...")
    
    for i, user in enumerate(users_with_stats, 1):
        role = getattr(user.profile, 'role', 'customer') if hasattr(user, 'profile') and user.profile else 'customer'
        print(f"\n   {i}. {user.get_full_name() or user.username} ({role})")
        print(f"      📧 {user.email}")
        print(f"      📅 Events: {user.events_posted} posted, {user.event_bookings_received} bookings received")
        print(f"      🏢 Venues: {user.venues_posted} posted, {user.venue_bookings_received} bookings received")
        print(f"      ⭐ Reviews: {user.event_reviews_given + user.venue_reviews_given} given (E:{user.event_reviews_given}, V:{user.venue_reviews_given})")
        print(f"      💬 Comments: {user.event_comments_posted + user.venue_comments_posted} posted (E:{user.event_comments_posted}, V:{user.venue_comments_posted})")
        print(f"      🎫 Bookings: {user.event_bookings_made + user.venue_bookings_made} made (E:{user.event_bookings_made}, V:{user.venue_bookings_made})")
        print(f"      📆 Joined: {user.date_joined.strftime('%B %d, %Y')}")
    
    print("\n" + "=" * 60)
    
    # Test top performers
    print("🏆 TOP PERFORMERS:")
    
    top_event_creators = User.objects.annotate(
        event_count=Count('organized_events')
    ).filter(event_count__gt=0).order_by('-event_count')[:5]
    
    print(f"   🎪 Top Event Creators:")
    for i, user in enumerate(top_event_creators, 1):
        print(f"      {i}. {user.get_full_name() or user.username}: {user.event_count} events")
    
    top_venue_creators = User.objects.annotate(
        venue_count=Count('managed_venues')
    ).filter(venue_count__gt=0).order_by('-venue_count')[:5]
    
    print(f"   🏢 Top Venue Owners:")
    for i, user in enumerate(top_venue_creators, 1):
        print(f"      {i}. {user.get_full_name() or user.username}: {user.venue_count} venues")
    
    print("\n" + "=" * 60)
    
    # Test content analytics
    print("📊 CONTENT ANALYTICS:")
    
    events_with_stats = Event.objects.annotate(
        review_total=Count('reviews', distinct=True),
        comment_total=Count('comments', distinct=True),
        avg_rating=Avg('reviews__rating'),
        booking_total=Count('bookings', distinct=True)
    ).select_related('organizer').order_by('-created_at')[:5]
    
    print(f"   📅 Recent Events with Stats:")
    for i, event in enumerate(events_with_stats, 1):
        avg_rating_str = f"{event.avg_rating:.1f}★" if event.avg_rating else "No ratings"
        print(f"      {i}. \"{event.title}\" by {event.organizer.get_full_name() or event.organizer.username}")
        print(f"         ⭐ {event.review_total} reviews ({avg_rating_str}) | 💬 {event.comment_total} comments | 🎫 {event.booking_total} bookings")
    
    venues_with_stats = Venue.objects.annotate(
        review_total=Count('reviews', distinct=True),
        comment_total=Count('comments', distinct=True),
        avg_rating=Avg('reviews__rating'),
        booking_total=Count('bookings', distinct=True)
    ).select_related('manager').order_by('-created_at')[:5]
    
    print(f"   🏢 Recent Venues with Stats:")
    for i, venue in enumerate(venues_with_stats, 1):
        avg_rating_str = f"{venue.avg_rating:.1f}★" if venue.avg_rating else "No ratings"
        print(f"      {i}. \"{venue.name}\" by {venue.manager.get_full_name() or venue.manager.username}")
        print(f"         ⭐ {venue.review_total} reviews ({avg_rating_str}) | 💬 {venue.comment_total} comments | 📅 {venue.booking_total} bookings")
    
    print("\n" + "=" * 60)
    
    # Test recent activity
    print("🎯 RECENT ACTIVITY:")
    
    recent_event_reviews = EventReview.objects.select_related('user', 'event').order_by('-created_at')[:5]
    print(f"   ⭐ Recent Event Reviews:")
    for i, review in enumerate(recent_event_reviews, 1):
        print(f"      {i}. {review.user.get_full_name() or review.user.username} reviewed \"{review.event.title}\" - {review.rating}★")
    
    recent_venue_reviews = VenueReview.objects.select_related('user', 'venue').order_by('-created_at')[:5]
    print(f"   🏢 Recent Venue Reviews:")
    for i, review in enumerate(recent_venue_reviews, 1):
        print(f"      {i}. {review.user.get_full_name() or review.user.username} reviewed \"{review.venue.name}\" - {review.rating}★")
    
    print("\n" + "=" * 60)
    print("✅ Enhanced Admin Dashboard Data Collection Test Complete!")
    print(f"🌐 Access the dashboard at: http://127.0.0.1:8000/auth/admin/dashboard/")
    
    return True

if __name__ == "__main__":
    test_admin_dashboard_data()