from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import JobForm
import pytz


def user_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request, f' Successfully logged in as {user.username}!')
            return redirect('home')
        except:
            if not User.objects.filter(email=email).exists():
                messages.error(request, "Account Not found. Please sign up using the below link.")
            elif not User.objects.get(email=email).profile.native_auth:
                messages.error(request, "You chose the Google sign-in method when you created your account. Please "
                                        "choose Google to sign in.")
            else:
                messages.error(request, "Username and Password didn't match, please try again!")

    elif request.method == 'GET':
        return render(request, 'registration/login.html')

    return render(request, 'registration/login.html', {'form': form, 'title': 'log in'})


def users_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('password')
        role = request.POST.get('inlineRadioOptions')
        time_zone = request.POST.get('userTimezone')
        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.profile.role = role
            user.profile.native_auth = True
            user.profile.time_zone = time_zone
            user.save()
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f' Account Successfully created for {user.username}!')
                return redirect('home')
            else:
                error = " Sorry! There was an error while registering your account, Please try again ! "
                messages.error(request, f' Sorry! There was an error while registering the account for {user.username},'
                                        f' Please try again!')
                return render(request, 'registration/signup.html', {"error": error})

        else:
            messages.error(request, "Account already exists. Please login.")
            return render(request, 'registration/login.html')

    elif request.method == 'GET':
        return render(request, 'registration/signup.html', {'timezones': pytz.common_timezones})

    else:
        error = " Unhandled Exception. Please try again"
        messages.error(request, "Account not created, please try again!")
        return render(request, 'registration/signup.html', {"error": error})


def users_profile(request):
    if request.user.is_authenticated:
        return render(request, 'home/profile.html')
    else:
        return redirect('login_url')


def users_jobs(request):
    if request.user.is_authenticated:
        return render(request, 'jobs/jobs.html')
    else:
        return redirect('login_url')

def users_jobDetails(request):
    if request.method == 'POST':
        form = JobForm(request.POST or None)
        # form.initial['user']=user
        # user = User.objects.filter(id = request.user.id)
        # form.fields['user'].label = user
        # print(form.fields['user'].label)
        if form.is_valid():
            form.save()
            # form.fields['user'].label = user
            # form.save()
            # user = request.user
            messages.success(request, ('Your Job has been saved successfully'))
            return render(request, 'jobs/jobDetails.html', {})
        else:
            messages.success(request, ('Error creating Job. Please try again'))
            return render(request, 'jobs/jobDetails.html', {})
    else:
        return render(request, 'jobs/jobDetails.html', {})


def users_reviews(request):
    if request.user.is_authenticated:
        return render(request, 'Reviews/reviews.html')
    else:
        return redirect('login_url')


def users_payments(request):
    if request.user.is_authenticated:
        return render(request, 'Payments/payments.html')
    else:
        return redirect('login_url')


def users_instructions(request):
    if request.user.is_authenticated:
        return render(request, 'home/instructions.html')
    else:
        return redirect('login_url')

