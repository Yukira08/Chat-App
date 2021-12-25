from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Room, Message
from accounts.models import User, Friendship
import json
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {})
    
@login_required
def room(request, room_name):
    try:
        a=Room.objects.get(name=room_name)
    except:
        a=Room.objects.create(name=room_name)
        a.save()

    # a= get_object_or_404(Room,name=room_name)
    if request.user not in a.participants.all():
        a.participants.add(request.user)
        a.save()
    
    messages = ""

    for message in Message.objects.filter(room = a):
        messages += message.sender.username + ': ' + message.message + '\n'
    

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'room_id' : mark_safe(json.dumps(a.id)),
        'messages' : mark_safe(json.dumps(messages))
    })