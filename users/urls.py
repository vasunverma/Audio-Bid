from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.user_login, name='login_url'),
    path('signup', views.users_signup, name='signup_url'),
    path('profile', views.users_profile, name='profile_url'),
    path('home/', views.users_home, name='homePage_url'),
    path('jobs/', views.users_jobs, name='jobs_url'),
    path('Reviews/', views.users_reviews, name='reviews_url'),
    path('Payments/', views.users_payments, name='payments_url'),
    path('instructions/', views.users_instructions, name='instructions_url'),
]