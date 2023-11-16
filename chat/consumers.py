from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from accounts.models import CustomUser


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.course_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print("connected", self.room_group_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("disconnect", self.room_group_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']

        user = await self.get_user_by_id(user_id)

        first_name = user.first_name
       

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'first_name': first_name,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        first_name = event['first_name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'first_name': first_name,
        }))

    @sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None    
