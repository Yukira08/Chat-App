# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_room', views.add_room, name='add_room'),
    path('create_room', views.create_room, name='create_room'),
    path('<str:room_name>/', views.room, name='room'),
    path('error', views.error, name = 'error'),
]