from django.urls import re_path

import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi())
]