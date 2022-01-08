
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'authtest/home.html')

@login_required
def private_page(request):
    return render(request, 'authtest/private.html', {})

def public_page(request):
    return render(request, 'authtest/public.html')

@login_required
def some_view(request):
    """Returns a json response to an ajax call. (request.user is available in view)"""
    data_attribute = request.GET.get('some_attribute')  # Make sure to use POST/GET correctly
    print(data_attribute)
    return JsonResponse(data={'data' : 'hello'}, status=200)