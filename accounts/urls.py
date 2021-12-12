from django.urls import path,include
from . import views
from authtest.views import home
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('signup', views.signup, name='signup'),
]