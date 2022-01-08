from django.urls import path,include
from . import views
from authtest.views import home
urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('signup', views.signup, name='signup'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('<str:friendname>/addfriend',views.add_friend,name='add_friend'),
    path('<str:friendname>/acceptfriend',views.accept_friend,name='accept_friend'),
    path('<str:friendname>/unfriend',views.unfriend,name='unfriend'),
    path('friends/search/', views.friend_search, name = 'friend_search'),
]
