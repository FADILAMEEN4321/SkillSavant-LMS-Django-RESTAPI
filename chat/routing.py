from django.urls import re_path
from .consumers import ChatRoomConsumer


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<course_id>\d+)/$', ChatRoomConsumer.as_asgi()),
]


