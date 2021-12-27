from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from .models import Room, Message
from accounts.models import User, Friendship
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {})

def error(request):
    return render(request, 'chat/error.html', {})


@login_required
def room(request, room_name):
    try:
        a=Room.objects.get(name=room_name)
        #print(a.id)
    except:
        return redirect(error)
        # a=Room.objects.create(name=room_name)
        # a.save()

    # a= get_object_or_404(Room,name=room_name)
    # print(request.user.username)
    # for b in a.participants.all():
    #     print(b.username)

    if request.user not in a.participants.all():
    #     # a.participants.add(request.user)
    #     # a.save()
        return redirect(error)
    


    messages = ""

    for message in Message.objects.filter(room = a):
        messages += message.sender.username + ': ' + message.message + '\n'
    

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'room_id' : mark_safe(json.dumps(a.id)),
        'messages' : mark_safe(json.dumps(messages))
    })



@login_required
def add_room(request):
    inst = Friendship.objects.filter(friends=request.user)
    friends = []
    for i in inst:
        friends.append(i.cur_user.username)

    return render(request, 'chat/add_room.html', {
        'friends' : friends
    })




@login_required
def create_room(request):
    
    if request.method=="POST":
        room_name = request.POST['room_name']
        friends = request.POST.getlist('friends')
        
        new_room=Room.objects.create(name=room_name)
        new_room.participants.add(request.user)

        for friend in friends:
            a = User.objects.get(username=friend)
            new_room.participants.add(a)
        new_room.save()
        return redirect(room, room_name=room_name)

    return redirect(error)

