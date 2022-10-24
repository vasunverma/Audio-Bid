from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


def home(request):
    if request.user.is_authenticated:
        if User.objects.get(id=request.user.id).profile.role == ''\
                or User.objects.get(id=request.user.id).profile.time_zone == '':
            messages.success(request, 'Please fill out the missing info')
            return redirect('users/profile')

    return render(request, 'home.html', {})
