from django.shortcuts import render,redirect
from django.contrib.auth import login as log
from accounts.forms import CustomUserCreationForm
from authtest.views import home
# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'accounts/signup.html',{'form':form})
