from django.shortcuts import render
from accounts.forms import CustomUserCreationForm
# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')

def signup(request):
    return render(request,'accounts/login.html') #fix to signup.html
