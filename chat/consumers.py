from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message, Room
from accounts.models import User
from datetime import datetime
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

        await self.online_update()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.offline_update()

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

    @database_sync_to_async
    def online_update(self):
        user = User.objects.get(id = self.scope['user'].id)
        user.online_status += 1
        user.save()
        #print(self.scope['user'].online_status)


    @database_sync_to_async
    def offline_update(self):
        user = User.objects.get(id = self.scope['user'].id)
        user.online_status -= 1
        user.offline_time = datetime.now()
        user.save()
        #print(self.scope['user'].online_status)

    # Receive message from room group
    async def chat_message(self, event): #when receiving (including the sender) # self = receiver
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))
