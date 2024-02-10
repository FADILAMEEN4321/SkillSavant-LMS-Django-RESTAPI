import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .prompts import assemble_prompt
from openai import OpenAI
from django.conf import settings
import asyncio


openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LearningPathConsumer(AsyncWebsocketConsumer):
    """
    LearningPathConsumer WebSocket consumer class.

    Handles WebSocket connections for streaming OpenAI chat completions
    for learning path course content. Clients send course name, server
    streams back AI-generated course content until end token.
    """

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        course_name = json.loads(text_data)["course_name"]

        messages = assemble_prompt(course_name)

        stream_response = openAI_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.2,
            max_tokens=80,
            stream=True,
        )

        for chunk in stream_response:
            if chunk.choices[0].delta.content is not None:
                await self.send(
                    text_data=json.dumps({"content": chunk.choices[0].delta.content})
                )
                await asyncio.sleep(0)
        await self.send(text_data=json.dumps({"content": "<:END:>"}))
