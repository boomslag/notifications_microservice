import json
from apps.notifications.models import Notification
from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
from channels.db import database_sync_to_async
import jwt
from django.conf import settings
secret_key = settings.SECRET_KEY


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user_id = self.scope['query_string'].decode('utf-8').split('=')[1]
        self.group_name = 'notification_'+self.user_id
        print(f'User {self.user_id} joined Websocket with Group name {self.group_name}')
        # Join Group
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
    # Receive message from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        if message_type == 'get_notifications':
            # Fetch notifications for user
            start = int(text_data_json.get('start', 0))
            count = int(text_data_json.get('count', 20))
            notification_data = await self.get_notifications(start, count)
            # Send notifications to WebSocket
            await self.send_notifications(notification_data)
        else:
            message = text_data_json['message']
            event = {
                'type': 'send_message',
                'message': message
            }
            await self.channel_layer.group_send(self.group_name, event)
            
    @database_sync_to_async
    def get_notifications(self, start, count):
        return list(Notification.objects.filter(to_user=self.user_id, is_seen=False).order_by('-date')[start:start+count].values('id', 'text_preview','notification_type','url','course','product','order','order_item','icon',))
    
    @database_sync_to_async
    def get_notification_count(self):
        return Notification.objects.filter(to_user=self.user_id, is_seen=False).count()
    
    async def send_notifications(self, event):
        total_count = await self.get_notification_count()
        message = {
            'type': 'notifications',
            'data': event,
            'total_count': total_count
        }
        await self.send(text_data=json.dumps(message))

    async def send_notifications_from_view(self, event):
        total_count = await self.get_notification_count()
        message = event['data']
        print(message)
        await self.send(text_data=json.dumps(message))

    async def send_message(self, event):
        message = event['message']
        # send message to websocket
        await self.send(text_data=json.dumps({'message':message}))
    
    async def send_notification(self, event):
        message = event['message']
        notification_data= {
            'id':str(message.get('id')),
            'course':str(message.get('course')),
            'product':str(message.get('product')),
            'order':str(message.get('order')),
            'order_item':str(message.get('order_item')),
            'thread':str(message.get('thread')),
            'from_user':str(message.get('from_user')),
            'to_user':str(message.get('to_user')),
            'notification_type':str(message.get('notification_type')),
            'text_preview':str(message.get('text_preview')),
            'url':str(message.get('url')),
            'is_seen':str(message.get('is_seen')),
            'icon':str(message.get('icon')),
        }
        total_count = await self.get_notification_count()
        message = {
            'type': 'new_notification',
            'data': notification_data,
            'total_count': total_count
        }
        # send message to websocket
        await self.send(text_data=json.dumps(message))