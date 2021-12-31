from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from .models import Room, Message, YourModelForm
from accounts.views import friendlist
from accounts.models import User, Friendship
import json
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'chat/index.html', {'friendnames':friendlist(request.user.username)})

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
    available_room=Room.objects.filter(participants=request.user).values('name')
    available_room=[x['name'] for x in available_room]
    available_room.remove(room_name)
    f=YourModelForm()
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'chat_rooms':available_room,
        'form': f,
    })

@login_required
def sf(request):
    return render(request,'chat/sf.html')