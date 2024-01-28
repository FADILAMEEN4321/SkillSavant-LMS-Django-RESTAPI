import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .prompts import assemble_prompt
from openai import OpenAI
from django.conf import settings
import asyncio


openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LearningPathConsumer(AsyncWebsocketConsumer):
    """
    LearningPathConsumer handles websocket connections for learning path creation.

    Key functions:

    - connect: Accepts the websocket connection.

    - disconnect: Handles disconnection.

    - receive: Receives text data from the websocket. Calls OpenAI API to create learning path.
    Sends response back over websocket.
    """

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        course_name = json.loads(text_data)["course"]

        messages = assemble_prompt(course_name)

        stream_response = openAI_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            max_tokens=500,
            stream=True,
        )

        for chunk in stream_response:
            if chunk.choices[0].delta.content is not None:
                await self.send(
                    text_data=json.dumps({"content": chunk.choices[0].delta.content})
                )
                await asyncio.sleep(0)
