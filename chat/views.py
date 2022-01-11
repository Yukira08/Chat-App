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
from django.db.models import Count
# Create your views here.
@login_required
def index(request):
    if Room.objects.filter(participants = request.user).count() ==0:
        new_room = Room.objects.create(name = "Welcome " + request.user.username + " to Kapter!")
        new_room.participants.add(request.user)
        new_room.save()
        return redirect(room,room_id=new_room.id)
    else:
        recent_msg=Message.objects.filter(sender=request.user).order_by('-date')
        for msg in recent_msg:
            if request.user in msg.room.participants.all():
                return redirect(room,room_id=msg.room.id)
        return_room = Room.objects.filter(participants = request.user)[0]
        return redirect(room,room_id=return_room.id)






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
        'room_name': a.name,
        'form': f,
        'messages' : Message.objects.filter(room = a),
        'notifications' : notifications,
        'unread_num' : unread_num,
    })

def checkajax(request):
    room_id = request.GET.get('room_id')  
    r=Room.objects.get(id=room_id)
    mess=Message.objects.filter(room=r)[0]
    return JsonResponse(data={"msg":mess.message}, status=200)



@login_required
def add_room(request):
    room_id = 0
    participant_list = []
    inst = Friendship.objects.filter(friends=request.user)
    friends = []
    room_name = None
    for i in inst:
        friends.append(i.cur_user.username)
        #print(i.cur_user.username)
    title = "Create room"

    if request.method=="POST":
        room_id = request.POST['room_id']
        
        room = Room.objects.get(id=room_id)
        room_name = room.name
        title = "Modify room " + room.name
        #print(title)
        for participant in room.participants.all():
            #print(participant.username)
            if participant.username in friends and participant.username != request.user.username:
                participant_list.append(participant.username)

        # return render(request, 'chat/add_room.html', {
        # 'friends' : friends
        # })

    return render(request, 'chat/add_room.html', {
        'friends' : friends,
        'title' : title,
        'participants' : mark_safe(json.dumps(participant_list)),
        'room_id' : room_id,
        'room_name' :  mark_safe(json.dumps(room_name)),
    })


@login_required
def create_room(request):
    
    if request.method=="POST":
        room_name = request.POST['room_name']
        friends = request.POST.getlist('friends')
        # print(request.POST['room_id'])
        #print("running")

        if request.POST['room_id'] != '0':
            cur_room = Room.objects.get(id=request.POST['room_id'])
            cur_room.name = room_name
            cur_room.participants.set([]) 
            cur_room.participants.add(request.user)
            for friend in friends:
                a = User.objects.get(username=friend)
                cur_room.participants.add(a)
            cur_room.save()
            return redirect(room, room_id=cur_room.id)
        #print(friends)
        mutualrooms=Room.objects.filter(participants__username__in=friends+[request.user.username])\
        .annotate(num_ptcpant=Count('participants')).filter(num_ptcpant=len(friends)+1)
        if len(mutualrooms)>0:
            return redirect(room,room_id=mutualrooms[0].id)
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
    #print(signal)

    notification = Notification.objects.filter(receiver = request.user, unread = True).order_by('-time')
    senders = []
    for n in notification:
        senders.append(n.sender.username)
    #print(notification.count())
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

@login_required
def friend(request):
    friends = Friendship.objects.filter(friends=request.user).all()
    for friend in friends:
        print(friend.cur_user.username)
    return render(request,'chat/friend.html' ,{"friends":friends})


def friend_search(request, friendname):
    friends = User.objects.filter(username__icontains=friendname)
    return render(request,'chat/friend_search.html', {"friends":friends})
