from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from accounts.models import CustomUser
from course.models import Course
from .models import ChatMessage



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

        # # Fetch historical messages from the database and send them to the client
        # await self.send_initial_messages()


        


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

        # Save the message to the database
        await self.save_message_to_database(user, message)
         

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'first_name': first_name,
                'user_id':user_id
            }
        )
    
    @sync_to_async
    def save_message_to_database(self, user, message):
        # Get the course instance based on the course_id in the consumer
        course_id = self.course_id
        course = Course.objects.get(id=course_id) 

         # Create and save the ChatMessage instance
        chat_message = ChatMessage(course=course, sender=user, message=message)
        chat_message.save()


    # @sync_to_async
    # def get_messages_from_database(self):
    #     # Get historical messages from the database
    #     course_id = self.course_id
    #     messages = ChatMessage.objects.filter(course_id=course_id).order_by('timestamp')
    #     return [{'message': msg.message, 'first_name': msg.sender.first_name, 'user_id': msg.sender.id} for msg in messages]


    # async def send_initial_messages(self):
    #     # Fetch historical messages from the database
    #     messages = await self.get_messages_from_database()

    #     # Send historical messages to the WebSocket
    #     for message in messages:
    #         await self.send(text_data=json.dumps(message))      



    async def chat_message(self, event):
        message = event['message']
        first_name = event['first_name']
        user_id = event['user_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'first_name': first_name,
            'user_id':user_id,
        }))


    @sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None    



