import os
import requests
import datetime
import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import JobForm
from .models import Job
from .models import Profile
from .filters import JobFilter
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from itertools import chain
from users.models import Job
from django.http import JsonResponse
from django.core import serializers
import logging
logger = logging.getLogger(__name__)

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


def user_logout(request):
    logout(request)
    return redirect('home')


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


def users_reset_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        messages.error(request, "Error occurred while sending reset email.")
                        return render(request, 'registration/password/password_reset.html')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return render(request, 'registration/password/password_reset.html')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def users_profile(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            selectedTimeZone = "UTC"
            if request.user.profile.time_zone != '':
                selectedTimeZone = request.user.profile.time_zone
            context = {
                'user': request.user,
                'timezones': pytz.common_timezones,
                'selectedTimeZone': selectedTimeZone
            }
            return render(request, 'home/profile.html', context)
        elif request.method == 'POST':
            user = User.objects.get(id=request.user.id)
            user.profile.time_zone = request.POST.get('userTimezone')
            user.save()
            context = {
                'user': request.user,
                'timezones': pytz.common_timezones,
                'selectedTimeZone': user.profile.time_zone
            }
            messages.success(request, f' Profile updated successfully for {user.username}!')
            return render(request, 'home/profile.html', context)
    else:
        return redirect('login_url')

def users_jobs(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get("formId") == "claimJobform":
                job_id = request.POST.get("jobIdToBeClaimed")
                job_to_be_claimed = Job.objects.get(id=job_id)
                job_to_be_claimed.worker_id = request.user.id
                job_to_be_claimed.status = 1
                job_to_be_claimed.save()
                messages.success(request, ('Your Job has been successfully claimed!'))

            else:
                form = JobForm(request.POST or None)
                form.instance.user = request.user
                if form.is_valid():
                    if request.POST.get("URL"):
                        check_gdrive(request.POST.get("URL"))
                        form.instance.url2audio = request.POST.get("URL")
                    elif "audiofile" in request.FILES:
                        extension = os.path.splitext(str(request.FILES['audiofile']))[1]
                        filename = filename_gen(str(request.user), extension)
                        default_storage.save(filename, request.FILES['audiofile'])
                        form.instance.url2audio = url_gen(filename)
                    elif "recorded" in request.FILES:
                        filename = filename_gen(str(request.user), ".wav")
                        default_storage.save(filename, request.FILES['recorded'])
                        form.instance.url2audio = url_gen(filename)
                    form.save()
                    messages.success(request, ('Your Job has been created successfully'))
                else:
                    messages.error(request, ('Error creating Job. Please try again'))

            return redirect('jobs_url')

        elif request.method == 'GET':
            is_creator = False
            if request.user.profile.role == 'creator':
                post_list = Job.objects.filter(Q(user_id=request.user.id))
                is_creator = True
            else:
                post_list = Job.objects.filter(Q(worker_id=request.user.id))
                post_list = list(chain(post_list, Job.objects.filter(Q(worker_id=0))))

            page = request.GET.get('page', '1')
            paginator = Paginator(post_list, 10)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            badge_classes = {
                'AVAILABLE': 'badge-primary',
                'INPROGRESS': 'badge-warning',
                'COMPLETED': 'badge-success',
                'CANCELLED': 'badge-danger'
            }
            myFilter = JobFilter()
            for job in posts:
                job.status = job.status_choices[job.status][1]
                job.status_badge = badge_classes[job.status]
                job.price = "{:.2f}".format(job.price)

            return render(request, 'jobs/jobs.html', {'page': page,
                                                      'posts': posts,
                                                      'myFilter': myFilter,
                                                      'creator': is_creator})
    else:
        return redirect('login_url')


def users_edit_job(request, id):
    if request.user.is_authenticated:
        job = Job.objects.get(id=id)
        if request.method == 'POST':
            form = JobForm(request.POST, instance=job)
            if form.is_valid():
                if request.POST.get("URL"):
                    check_gdrive(request.POST.get("URL"))
                    form.instance.url2audio = request.POST.get("URL")
                elif "audiofile" in request.FILES:
                    extension = os.path.splitext(str(request.FILES['audiofile']))[1]
                    filename = filename_gen(str(request.user), extension)
                    default_storage.save(filename, request.FILES['audiofile'])
                    form.instance.url2audio = url_gen(filename)
                elif "recorded" in request.FILES:
                    filename = filename_gen(str(request.user), ".wav")
                    default_storage.save(filename, request.FILES['recorded'])
                    form.instance.url2audio = url_gen(filename)
                form.save()
                messages.success(request, ('Your Job has been updated successfully'))
                return redirect('jobs_url')
            else:
                messages.error(request, ('Error updating Job. Please try again'))
        else:
            return JsonResponse({
                "name": job.name,
                "description": job.description,
                "end_date": job.end_date.strftime("%Y-%m-%d"),
                "price": "{0:.2f}".format(job.price)

            }, status=200)   
    else:
        return redirect('login_url')
    
    
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


# Helpers
def check_gdrive(url):
    response = requests.get(url)
    if 'drive.google.com' not in response.url or 'ServiceLogin' in response.url:
        print("Invalid URL: " + url)


def filename_gen(user, ext):
    return str(datetime.datetime.now().timestamp()).replace('.', '-') + "-" + user + ext


def url_gen(filename):
    return "https://" + os.environ['bucket_name'] + ".s3." + os.environ['aws_region'] + ".amazonaws.com/" + filename
