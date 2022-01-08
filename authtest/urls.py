from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('priv', views.private_page, name='priv'),
    path('pub', views.public_page, name='pub'),
    path('some-view-does-something/', views.some_view, name='doing-something'),
]