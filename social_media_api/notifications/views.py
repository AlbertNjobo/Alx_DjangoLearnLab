from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationListView(APIView):
    """View to fetch notifications for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        data = [{'id': n.id, 'verb': n.verb, 'timestamp': n.timestamp} for n in notifications]
        return Response(data)
