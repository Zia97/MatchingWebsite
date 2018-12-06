from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='index'), #redirects user if already logged in
    path('register', views.register, name = 'register'),
    path('home', views.home, name = 'home')
]
