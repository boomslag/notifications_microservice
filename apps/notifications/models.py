from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Notification(models.Model):
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Followed'), (4, 'Purchased'), (5, 'Delivery'), (6, 'Message'))
    
    course = models.CharField(max_length=256,blank=True, null=True)
    product = models.CharField(max_length=256,blank=True, null=True)
    order = models.CharField(max_length=256,blank=True, null=True)
    order_item = models.CharField(max_length=256,blank=True, null=True)
    thread = models.CharField(max_length=256,blank=True, null=True)

    from_user = models.CharField(max_length=256,blank=True, null=True)
    to_user = models.CharField(max_length=256,blank=True, null=True)

    icon = models.CharField(max_length=256,blank=True, null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.TextField(blank=True)
    
    url = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Convert UUID fields to strings
        self.course = str(self.course) if self.course else None
        self.product = str(self.product) if self.product else None
        self.order = str(self.order) if self.order else None
        self.order_item = str(self.order_item) if self.order_item else None
        self.thread = str(self.thread) if self.thread else None
        self.icon = str(self.icon) if self.icon else None

        super().save(*args, **kwargs)

    def created(self, *args, **kwargs):
        self.save()
        
        # Send message to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notification_{self.to_user}",  # client's channel name
            {
                'type': 'send_notification',
                'message': {
                    'id': str(self.id),
                    'course': self.course,
                    'product': self.product,
                    'order': self.order,
                    'order_item': self.order_item,
                    'thread': self.thread,
                    'from_user': self.from_user,
                    'to_user': self.to_user,
                    'notification_type': self.notification_type,
                    'text_preview': self.text_preview,
                    'url': self.url,
                    'is_seen': self.is_seen,
                    'icon': self.icon,
                },
            },
        )