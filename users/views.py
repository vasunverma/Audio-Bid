from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = " Sorry! Username and Password didn't match, Please try again ! "
            return render(request, 'registration/login.html', {'error': error})
    else:
        return render(request, 'registration/login.html')


def users_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('password')
        role = request.POST.get('inlineRadioOptions')
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.profile.role = role
        user.profile.native_auth = True
        user.save()

        return HttpResponseRedirect("/")
    else:
        error = " Unhandled Exception. Please try again"
        return render(request, 'registration/signup.html', {"error": error})


def users_profile(request):
    if request.user.is_authenticated:
        return render(request, 'home/profile.html')
    else:
        return redirect('login_url')

def users_jobs(request):
    return render(request, 'jobs/jobs.html')

def users_reviews(request):
    return render(request, 'Reviews/reviews.html')

def users_payments(request):
    return render(request, 'Payments/payments.html')

def users_instructions(request):
    return render(request, 'home/instructions.html')
