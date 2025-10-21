from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('notifications/', views.notifications_list, name='notifications'),
    path('api/notification-count/', views.notification_count, name='notification_count'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_read, name='mark_all_read'),
]
