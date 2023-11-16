from django.urls import re_path
from .consumers import ChatRoomConsumer


# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<enrolled_course_id>\w+)/$', ChatRoomConsumer.as_asgi())
# ]

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<course_id>\d+)/$', ChatRoomConsumer.as_asgi()),
]
