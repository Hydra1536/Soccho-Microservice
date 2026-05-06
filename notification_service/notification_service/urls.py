from django.contrib import admin
from django.urls import path
from notifications.viewsets import NotificationViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/notifications/', NotificationViewSet.as_view({'get': 'list'})),
    path('api/notifications/mark-read/', NotificationViewSet.as_view({'post': 'mark_read'})),
    path('api/notifications/unread-count/', NotificationViewSet.as_view({'get': 'unread_count'})),
]

