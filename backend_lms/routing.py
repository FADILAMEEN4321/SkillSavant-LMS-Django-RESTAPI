from django.urls import re_path, path
from chat.consumers import ChatRoomConsumer
from openai_api.consumers import LearningPathConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<course_id>\d+)/$', ChatRoomConsumer.as_asgi()),
    path('ws/learning-path-creation', LearningPathConsumer.as_asgi())
]

