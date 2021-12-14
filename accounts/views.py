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
    if request.user.username == username:
        data['option']= False
    else:
        data['option']= True
    inst=User.objects.get(username=username)
    data['username']=inst.username
    data['email']=inst.email
    return render(request,'accounts/profile.html',data)