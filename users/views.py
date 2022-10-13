from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout,login
from django.http import HttpResponse, HttpResponseRedirect

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(request,user)
            return redirect('profile_url')
        else:
            error = " Sorry! Username and Password didn't match, Please try again ! "
            return render(request, 'registration/login.html',{'error':error})
    else:
        return render(request, 'registration/login.html')

def users_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        pass_1 = request.POST.get('password')
        pass_2 = request.POST.get('password1')
        if pass_1 == pass_2:
             user = User.objects.create_user(
                                              username=email,
                                              first_name=first_name,
                                              last_name=last_name,
                                              email=email,
                                              password=pass_1,
                                             )
             return HttpResponseRedirect("/")
        else:
             error = " Password Mismatch "
             return render(request, 'registration/signup.html',{"error":error})
    else:
         return render(request, 'registration/signup.html')

def users_profile(request):
    if request.user.is_authenticated:
        return render(request, 'home/profile.html')
    else:
        return redirect('login_url')