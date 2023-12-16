import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )