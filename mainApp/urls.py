from django.urls import path
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', user_views.user_login, name='login_url'),
]