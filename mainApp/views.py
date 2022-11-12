from django.shortcuts import render
from django.contrib.auth.models import User
import pytz
#import sys
from users.models import Job
from django.db.models.query_utils import Q
#sys.path.insert(1, '/audiobidV1/users/models')

def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.user.profile.role == 'creator':
            num_created_jobs = Job.objects.filter(Q(user=request.user)).count()
            num_completed_jobs = Job.objects.filter(Q(user=request.user) & Q(status=2)).count()
            num_progress_jobs = Job.objects.filter(Q(user=request.user) & Q(status=1)).count()
            num_claimed_jobs = Job.objects.filter(Q(user=request.user) & Q(status=0)).count()
        elif request.user.profile.role == 'worker':
            num_created_jobs = 0
            num_completed_jobs = Job.objects.filter(Q(worker_id=request.user.id) & Q(status=2)).count()
            num_progress_jobs = Job.objects.filter(Q(worker_id=request.user.id) & Q(status=1)).count()
            num_claimed_jobs = Job.objects.filter(Q(worker_id=request.user.id) & Q(status=0)).count()

        print(num_created_jobs)
        print(num_completed_jobs)
        print(num_progress_jobs)
        print(num_claimed_jobs)
        if request.method == 'GET':
            if User.objects.get(id=request.user.id).profile.role == ''\
                    or User.objects.get(id=request.user.id).profile.time_zone == '':

                selectedTimeZone = "UTC"
                if user.profile.time_zone != '':
                    selectedTimeZone = user.profile.time_zone

                selectedRoleType = user.profile.role
                if selectedRoleType == '':
                    selectedRoleType = 'worker'

                nonSelectedRoleType = 'creator'
                if selectedRoleType == 'creator':
                    nonSelectedRoleType = 'worker'
    
                return render(request, 'home.html', {"MissingInfo": True,
                                                     "fname": user.first_name,
                                                     "lname": user.last_name,
                                                     "username": user.username,
                                                     "email": user.email,
                                                     "selectedRoleType": selectedRoleType,
                                                     "nonSelectedRoleType": nonSelectedRoleType,
                                                     "selectedTimeZone": selectedTimeZone,
                                                     'timezones': pytz.common_timezones,
                                                     'num_created_jobs': num_created_jobs, 
                                                     'num_completed_jobs': num_completed_jobs,
                                                     'num_progress_jobs': num_progress_jobs,
                                                     'num_claimed_jobs': num_claimed_jobs})
            else:
                return render(request, 'home.html', {"MissingInfo": False,
                                                     'num_created_jobs': num_created_jobs, 
                                                     'num_completed_jobs': num_completed_jobs,
                                                     'num_progress_jobs': num_progress_jobs,
                                                     'num_claimed_jobs': num_claimed_jobs})


        elif request.method == 'POST':
            user.profile.role = request.POST.get('inlineRadioOptions')
            user.profile.time_zone = request.POST.get('userTimezone')
            user.save()
            render(request, 'home.html', {"MissingInfo": False,
                                          'num_created_jobs': num_created_jobs, 
                                          'num_completed_jobs': num_completed_jobs,
                                          'num_progress_jobs': num_progress_jobs,
                                          'num_claimed_jobs': num_claimed_jobs})

    return render(request, 'home.html', {"MissingInfo": False})
