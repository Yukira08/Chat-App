from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message, Room
import json
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_id']
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
        message = text_data_json['message']
        room_id = text_data_json['room_id']
        user= self.scope['user']
        await self.save_message(message, room_id)
        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     { 'type': 'chat_message', 'message': user.username+":"+message}
        # )    
        await self.channel_layer.group_send(
            self.room_group_name,
            { 'type': 'chat_message', 'message' : user.username + ': ' + message   + '\n'}
        )    

    @database_sync_to_async
    def save_message(self,message,room_id):
        room = Room.objects.get(id=room_id)

        a=Message.objects.create(sender=self.scope['user'],room = room, message=message)
        a.save()

        a = Message.objects.filter(sender=self.scope['user'],room = room, message = message).last()
        a.delete()

    # Receive message from room group
    async def chat_message(self, event): #when receiving (including the sender) # self = receiver
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
