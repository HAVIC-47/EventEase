from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Notification

@login_required
def notifications_list(request):
    """Display user's notifications with pagination"""
    notifications = Notification.objects.filter(user=request.user)
    
    # Pagination
    paginator = Paginator(notifications, 10)  # Show 10 notifications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Mark all as read when viewing the list
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)
    
    context = {
        'page_obj': page_obj,
        'notifications': page_obj,
        'total_notifications': notifications.count(),
    }
    
    return render(request, 'core/notifications.html', context)

@login_required
def notification_count(request):
    """Get unread notification count for the current user"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, 'Notification marked as read.')
    return redirect('core:notifications')

@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read for the current user"""
    count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'marked_count': count})
    
    messages.success(request, f'Marked {count} notifications as read.')
    return redirect('core:notifications')

def create_notification(user, title, message, notification_type='system', **kwargs):
    """Helper function to create notifications"""
    return Notification.create_notification(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        **kwargs
    )
