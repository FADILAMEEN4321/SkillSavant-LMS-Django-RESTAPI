from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# import chat.routing
# from django.core.asgi import get_asgi_application


# django_asgi_app = get_asgi_application()


# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": 
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
# })

from django.urls import re_path
from chat.consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<course_id>\d+)/$', ChatRoomConsumer.as_asgi()),
]

