# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_room', views.add_room, name='add_room'),
    path('create_room', views.create_room, name='create_room'),
    path('<int:room_id>/', views.room, name='room'),
    path('checkajax/', views.checkajax, name='checkajax'),
    path('error', views.error, name = 'error'),
    path('test/test',views.sf,name='sf'),
    path('test',views.test,name='test'),
    path('<int:room_id>/search/', views.message_search, name = 'message_search'),
    path('load_noti/', views.load_noti, name='load_noti'),
    path('read_noti/<int:noti_id>/', views.read_noti, name = 'read_noti'),
    path('friend',views.friend,name='friend'),
    path('friend_search/<str:friendname>',views.friend_search,name='friend_search'),
]