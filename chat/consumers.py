from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message,Room
import json
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # self.user=self.scope["user"]
        # Join room group
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
    # Receive message from WebSocket
    async def receive(self, text_data): #when sending message
        text_data_json = json.loads(text_data)
        try:
            message = text_data_json['message']
            await self.save_message(message)
        except:
            message='send file'
            files = text_data_json['raw']
            print(type(files))
            print(files)
        user=self.scope['user']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            { 'type': 'chat_message', 'message': user.username+":"+message}
        )    
    @database_sync_to_async
    def save_message(self,message):
        a=Message.objects.create(sender=self.scope['user'],message=message)
        a.save()
    # Receive message from room group
    async def chat_message(self, event): #when receiving (including the sender) # self = receiver
        message = event['message']
        # a=Message.objects.create(sender=self.scope['user'],message=message)
        # a.save()
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
