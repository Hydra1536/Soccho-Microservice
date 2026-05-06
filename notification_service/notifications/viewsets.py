from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).select_related('recipient').order_by('-created_at')

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        ids = request.data.get('ids', [])
        Notification.objects.filter(id__in=ids, recipient=request.user).update(is_read=True)
        return Response({'marked': len(ids)})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'count': count})

