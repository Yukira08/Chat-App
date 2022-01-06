from django.shortcuts import render,redirect
from django.contrib.auth import login as log
from accounts.forms import CustomUserCreationForm, ProfileUpdateForm
from authtest.views import home
from accounts.models import User, Friendship
from django.contrib import messages
# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/login.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            log(request,user)
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
        img_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if img_form.is_valid():
            img_form.save()
            messages.success(request,'Profile picture updated')
            return redirect('profile',username=request.user.username)
    else:
        img_form=ProfileUpdateForm(instance=request.user)
    data={}
    friendnames = []
    friend_number = 0
    inst=User.objects.get(username=username)
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
    if request.user==inst:
        data['option']= False
        data['per']=True
    else:
        data['per']=False
        if request.user.username in data['friendnames']:
            data['option'] = False
        else:
            data['option']= True

    return render(request,'accounts/profile.html',data)

def add_friend(request, friendname):
    inst=User.objects.get(username=friendname)
    Friendship.make_friend(request.user, inst)
    Friendship.make_friend(inst, request.user)

    return profile(request, friendname)


def friend_search(request):
    if request.method=='POST':
        username = request.POST['search_input']
        friends = User.objects.filter(username__icontains = username)
        return render(request, 'accounts/friend_lists.html', {
            'friends' : friends,
        })

    else:
        return redirect('home')