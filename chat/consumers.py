from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Message, Room, RoomCache
#from .models import NEW_MESSAGE_TYPE, FRIEND_REQUEST_TYPE
from accounts.models import Notification, User
from datetime import datetime
import json
from django.conf import settings
import os


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #print("Connecting to socket")
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

        await self.participants_cache_add(self.scope['url_route']['kwargs']['room_id'])

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.offline_update()

        await self.participants_cache_delete(self.scope['url_route']['kwargs']['room_id'])

    # Receive message from WebSocket
    async def receive(self, text_data): #when sending message
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id=text_data_json['room_id']
        filename=text_data_json.get("filename")
        filetype=text_data_json.get("filetype")
        filebin=text_data_json.get("filebin")
        time=datetime.now()
        await self.save_message(message,room_id,time,filename,filetype,filebin)
        getpath=''
        if filename!=None:
            getpath=str(settings.MEDIA_URL)+'upload/'+str(room_id)+'/'+time.strftime("%Y%m%d%H%M%S%f")+filename
        user=self.scope['user']

        # Send message to room group  
        await self.channel_layer.group_send(
            self.room_group_name,
            { 'type': 'chat_message', 'usrname': user.username,'message':message,'location': getpath,'filetype':filetype,'filename':filename}
        )    

    @database_sync_to_async
    def save_message(self,message,room_id,time,name=None,type=None,binn=None):
        print("receiving message")
        room = Room.objects.get(id=room_id)
        a=Message.objects.create(sender=self.scope['user'],room = room, date=time,message=message,filename=name)
        if name!=None:
            location=str(settings.MEDIA_ROOT)+'/upload/'+ str(a.room.id) 
            if not os.path.exists(location):
                os.makedirs(location)
            location += '/'+a.date.strftime("%Y%m%d%H%M%S%f")+name
            a.path=location
            data=bytes(list(binn.values()))
            f=open(location,'wb+')
            f.write(data)
            f.close()
        a.save()
        a = Message.objects.filter(sender=self.scope['user'],room = room, message = message).last()
        #a.delete()


        #send notification
        room_cache = RoomCache.objects.get(room = room)
        participants = room.participants.all()
        #print(participants)
        present_participants = room_cache.participants.all()
        #print(present_participants)
        for participant in participants:
            if participant not in present_participants:
                #print(participant)
                notification = Notification.objects.create(sender = self.scope['user'], receiver = participant, noti_type = 1, time = time, destination = room_id)
                notification.save()
                print(notification.receiver.username)


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
        usrname=event["usrname"]
        location=event["location"]
        filetype=event["filetype"]
        filename=event["filename"]
        # a=Message.objects.create(sender=self.scope['user'],message=message)
        # a.save()
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'usrname': usrname,'message':message,'location': location,"filetype":filetype,'filename':filename}))

    @database_sync_to_async
    def participants_cache_add(self, room_id):
        room = Room.objects.get(id=room_id)
        try:
            room_cache = RoomCache.objects.get(room = room)
        except:
            room_cache = RoomCache.objects.create(room = room)
        #room_cache.save()
        room_cache.participants.add(self.scope['user'])
        room_cache.save()
        print(room_cache.participants.all())

    @database_sync_to_async
    def participants_cache_delete(self, room_id):
        room = Room.objects.get(id=room_id)
        room_cache = RoomCache.objects.get(room = room)
        # try:
        #     room_cache = RoomCache.objects.get(room = room)
        # except:
        #     room_cache = RoomCache.objects.create(room = room)
        #room_cache.save()
        room_cache.participants.remove(self.scope['user'])
        room_cache.save()
        print(room_cache.participants.all())