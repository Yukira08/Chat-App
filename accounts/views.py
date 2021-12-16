from django.shortcuts import render,redirect
from django.contrib.auth import login as log
from accounts.forms import CustomUserCreationForm
from authtest.views import home
from accounts.models import User, Friendship
# Create your views here.
def login(request):
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

def profile(request,username):
    data={}
    friendnames = []
    inst=User.objects.get(username=username)
    data['user']=inst
    Friendship.objects.filter(friends=inst)

    for i in Friendship.objects.filter(friends=inst):
        friendnames.append(i.cur_user.username)

    data['friendnames'] = friendnames

    if request.user==inst:
        data['option']= False
    else:
        if request.user.username in friendnames:
            data['option'] = False
        else:
            data['option']= True

    return render(request,'accounts/profile.html',data)

def add_friend(request, friendname):
    inst=User.objects.get(username=friendname)
    Friendship.make_friend(request.user, inst)
    Friendship.make_friend(inst, request.user)

    return profile(request, friendname)
