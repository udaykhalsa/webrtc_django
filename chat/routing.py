from django.urls import path, re_path
from .consumers import VideoCalling

websocket_urlpatterns = [
  re_path('video/', VideoCalling.as_asgi())
]