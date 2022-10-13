from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login_url'),
    path('signup', views.users_signup, name='signup_url'),
    path('profile', views.users_profile, name='profile_url'),
]