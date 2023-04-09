
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer

from rest_framework import status
from rest_framework import permissions
from rest_framework_api.views import StandardAPIView

from .utils.auth import validate_token
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ListUserNotificationsView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        # try:
            payload = validate_token(request)
            user_id = payload['user_id']
            notifications = Notification.objects.filter(to_user=user_id, is_seen=False)
            serializer = NotificationSerializer(notifications,many=True)
            print(serializer.data)
            return self.paginate_response(request, serializer.data)
        # except Exception as e:
        #     return self.send_error(str(e), status=status.HTTP_404_NOT_FOUND)


class MarkAsSeenView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def put(self, request, *args, **kwargs):
        payload = validate_token(request)
        user_id = payload['user_id']
        notification_id = self.request.data.get('id')
        if notification_id:
            notification = Notification.objects.filter(to_user=user_id, id=notification_id, is_seen=False).first()
            if notification:
                notification.is_seen = True
                notification.save()

                # Notify the sender that the notification is seen
                notifications = Notification.objects.filter(to_user=user_id, is_seen=False).order_by('-date')[:20]
                notifications_data = list(notifications.values('id', 'text_preview', 'notification_type', 'url', 'course', 'product', 'order', 'order_item', 'icon'))

                 # Create message to send to WebSocket
                message = {
                    'type': 'send_notifications_from_view',
                    'data': notifications_data,
                }
            
                # Get channel layer and group name
                channel_layer = get_channel_layer()
                group_name = f'notification_{user_id}'

                # Send message to WebSocket group
                async_to_sync(channel_layer.group_send)(group_name, message)

        return self.send_response("Success")