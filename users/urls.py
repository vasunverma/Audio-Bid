from django.urls import path, include
from . import views
from users import views as user_views
from .views import line_chart, line_chart_json

urlpatterns = [
    path('login', views.user_login, name='login_url'),
    path("logout", views.user_logout, name= "logout"),
    path('signup', views.users_signup, name='signup_url'),
    path('profile', views.users_profile, name='profile_url'),
    path('jobs/', views.users_jobs, name='jobs_url'),
    path('Reviews/', views.users_reviews, name='reviews_url'),
    path('Payments/', views.users_payments, name='payments_url'),
    path('instructions/', views.users_instructions, name='instructions_url'),
    path("reset_password", views.users_reset_password, name="password_reset"),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]