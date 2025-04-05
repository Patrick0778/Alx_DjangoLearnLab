from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        if pk:
            # Mark single notification as read
            notification = Notification.objects.filter(
                recipient=request.user,
                id=pk,
                is_read=False
            ).first()
            
            if notification:
                notification.is_read = True
                notification.save()
                return Response({'message': 'Notification marked as read'})
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            # Mark all notifications as read
            Notification.objects.filter(
                recipient=request.user,
                is_read=False
            ).update(is_read=True)
            return Response({'message': 'All notifications marked as read'})
