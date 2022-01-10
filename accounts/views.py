from django.shortcuts import render,redirect
from django.contrib.auth import login as log
from accounts.forms import CustomUserCreationForm, ProfileUpdateForm
from authtest.views import home
from accounts.models import Notification, User, Friendship, FriendRequest
from django.contrib import messages
from datetime import datetime
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(index)
    return render(request, 'accounts/login.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            #log(request,user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'accounts/signup.html',{'form':form})
def friendlist(username):
    friendnames = []
    friend_number = 0
    inst=User.objects.get(username=username)
    fr=Friendship.objects.filter(friends=inst)
    for i in fr:
        friendnames.append(i.cur_user.username)
    return friendnames


def profile(request,username):
    
    friendnames = friendlist(request.user.username)
    if request.method=='POST':
        print("Change pic")
        img_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if img_form.is_valid():
            img_form.save()
            messages.success(request,'Profile picture updated')
            print("Change done")
            return redirect('profile',username=request.user.username)
    else:
        img_form=ProfileUpdateForm(instance=request.user)
    data={}
    friendnames = []
    friend_number = 0
    inst=User.objects.get(username=username)
    print(inst.img.url)
    data['room_id'] = 0
    data['user']=inst
    data['img_form']=img_form
    Friendship.objects.filter(friends=inst)
    data['offline_time'] = inst.offline_time

    if inst.online_status > 0:
        data['online'] = True
        #print( inst.online_status)
    else:
        data['online'] = False

    #print(data['online'])
    for i in Friendship.objects.filter(friends=inst):
        friendnames.append(i.cur_user.username)
        friend_number+=1

    data['friendnames'] = friendnames
    data['friend_number'] = friend_number
    data['img_form']=img_form

    data['accept_friend'] = False
    data['add_friend'] = False
    data['request_sent'] = False
    
    if request.user==inst:
        data['option']= False
        data['per']=True
    else:
        data['per']=False
        if request.user.username in data['friendnames']:
            data['option'] = False

        else:
            data['option']= True
            if FriendRequest.objects.filter(sender=inst, receiver= request.user, accepted = False).exists():
                data['accept_friend'] = True
                print("first stop")
            else :
                if FriendRequest.objects.filter(sender=request.user, receiver=inst, accepted = False).exists():
                    data['request_sent'] = True
                else :
                    data['add_friend'] = True
                    print("third stop")

    # print(data['add_friend'])
    # print(data['accept_friend'])
    return render(request,'accounts/profile.html',data)

def add_friend(request, friendname):
    inst=User.objects.get(username=friendname)
    try:
        friend_req = FriendRequest.objects.get(sender = request.user, receiver = inst)
    except:
    #inst=User.objects.get(username=friendname)
        friend_req = FriendRequest.objects.create(sender = request.user, receiver = inst)
        friend_req.save()
        notification = Notification.objects.create(sender = friend_req.sender, receiver = friend_req.receiver, noti_type = 2, time = datetime.now(), destination = friend_req.sender.id)
        notification.save()
    return redirect(profile, username = friendname)

def accept_friend(request, friendname):
    try:
        inst=User.objects.get(username=friendname)
        friend_request = FriendRequest.objects.get(sender=inst, receiver=request.user, accepted=False)
        friend_request.accepted = True
        friend_request.save()

        notification = Notification.objects.create(sender = request.user, receiver = inst, noti_type = 3, time = datetime.now(), destination = friend_request.receiver.id)
        notification.save()

        Friendship.make_friend(request.user, inst)
        Friendship.make_friend(inst, request.user)
        return redirect(profile, username = friendname)
    except:
        return redirect(profile, username = friendname)

def unfriend(request, friendname):
    inst=User.objects.get(username=friendname)
    Friendship.unfriend(request.user, inst)
    Friendship.unfriend(inst, request.user)
    return redirect(profile, username = friendname)



def friend_search(request):
    if request.method=='POST':
        username = request.POST['search_input']
        friends = User.objects.filter(username__icontains = username)
        return render(request, 'accounts/friend_lists.html', {
            'friends' : friends,
        })

    else:
        return redirect('home')