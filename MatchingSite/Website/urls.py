from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True),
         name='index'),  # redirects user if already logged in
    path('register', views.register, name='register'),
    path('users/', views.users, name='users'),
    path('allUsers/', views.allUsers, name='allUsers'),
    path('like/', views.like, name='like'),
    path('home', views.home, name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
