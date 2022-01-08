from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from .models import Room, Message, RoomCache, YourModelForm
from accounts.views import friendlist
from accounts.models import Notification, User, Friendship
import json
from accounts.views import profile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
import json

# Create your views here.

def index(request):
    return render(request, 'chat/index.html', {'friendnames':friendlist(request.user.username)})

def error(request):
    return render(request, 'chat/error.html', {})


@login_required
def room(request, room_id):
    try:
        a=Room.objects.get(id=room_id)
    except:
        return redirect(error)
    if request.user not in a.participants.all():
        return redirect(error)
    
    messages = ""

    # for message in Message.objects.filter(room = a):
    #     messages += message.sender.username + ': ' + message.message + '\n'
    #     a.participants.add(request.user)
    #     a.save()

    #cur_room = Room.objects.get(id=room_id)

    available_room=Room.objects.filter(participants=request.user)
    # available_room.remove(cur_room)
    f=YourModelForm()
    notifications = Notification.objects.filter(receiver = request.user)
    unread_num = Notification.objects.filter(receiver = request.user, unread=True).count()

    return render(request, 'chat/room.html', {
        'room_id' : mark_safe(json.dumps(room_id)),
        'messages' : mark_safe(json.dumps(messages)),
        'chat_rooms':available_room,
        'this_room' : room_id,
        'form': f,
        'messages' : Message.objects.filter(room = a),
        'notifications' : notifications,
        'unread_num' : unread_num,
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

        #room_cache = RoomCache.objects.create(room = new_room)
        #room_cache.save()
        return redirect(room, room_id=new_room.id)

    return redirect(error)

@login_required
def sf(request):
    return render(request,'chat/sf.html')

def test(request):
    return render(request,'chat/copy_code.html')
@login_required
def message_search(request, room_id):

    if request.method== "POST":
        search_input = request.POST['search_input']
        cur_room = Room.objects.get(id=room_id)
        messages = Message.objects.filter(room = cur_room, message__icontains = search_input)
        return render(request, 'chat/message_search.html', {
            'messages' : messages,
            'search': mark_safe(json.dumps(search_input)),
        })
    else:
        return redirect(error)


@login_required
def load_noti(request):
    signal = request.GET.get('signal')  
    print(signal)

    notification = Notification.objects.filter(receiver = request.user, unread = True)
    senders = []
    for n in notification:
        senders.append(n.sender.username)
    print(notification.count())
    return JsonResponse(data={"notification":list(notification.values()), "senders":senders}, status=200)

@login_required
def read_noti(request, noti_id):
    notification = Notification.objects.get(id = noti_id)
    notification.unread = False
    notification.save()
    if  notification.noti_type == 1:
        return redirect(room, room_id=notification.destination)
    else:
        return redirect(profile, notification.sender.username)

