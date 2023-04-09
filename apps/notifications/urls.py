from django.urls import path
from .views import *


urlpatterns = [
    path('get/', ListUserNotificationsView.as_view()),
    path('seen/', MarkAsSeenView.as_view()),
]