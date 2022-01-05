# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_room', views.add_room, name='add_room'),
    path('create_room', views.create_room, name='create_room'),
    path('<int:room_id>/', views.room, name='room'),
    path('error', views.error, name = 'error'),
    path('test/test',views.sf,name='sf'),
    path('test',views.test,name='test'),
]