from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.user_login, name='login_url'),
    path("logout", views.user_logout, name= "logout"),
    path('signup', views.users_signup, name='signup_url'),
    path('profile', views.users_profile, name='profile_url'),
    path("jobs/<int:id>/", views.users_edit_job, name="edit_job_url"),
    path('jobs/', views.users_jobs, name='jobs_url'),
    path("jobs/detail/", views.users_detail_job, name="detail_job_url"),
    path('Reviews/', views.users_reviews, name='reviews_url'),
    path('Payments/', views.users_payments, name='payments_url'),
    path('instructions/', views.users_instructions, name='instructions_url'),
    path("reset_password", views.users_reset_password, name="password_reset"),
]