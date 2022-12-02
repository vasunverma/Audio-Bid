from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import pytz
from users.models import Job
from django.db.models.query_utils import Q

def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.user.profile.role == 'creator':
            creatorJobs = Job.objects.filter(Q(user=request.user))
            num_created_jobs = len(creatorJobs)
            num_open_jobs, num_progress_jobs, num_completed_jobs = 0, 0, 0
            for jobs in creatorJobs:
                if jobs.status == 0:
                    num_open_jobs +=1 
                elif jobs.status == 1:
                    num_progress_jobs +=1
                elif jobs.status == 2:
                    num_completed_jobs +=1
        elif request.user.profile.role == 'worker':
            workerJobs = Job.objects.filter(Q(worker_id=request.user.id))
            num_created_jobs, num_open_jobs, num_progress_jobs, num_completed_jobs = 0, 0, 0, 0
            for jobs in workerJobs:
                if jobs.status == 1:
                    num_progress_jobs +=1
                elif jobs.status == 2:
                    num_completed_jobs +=1
                    
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
                                                     'timezones': pytz.common_timezones})
            else:
                return render(request, 'home.html', {"MissingInfo": False,
                                                     'num_created_jobs': num_created_jobs,
                                                     'num_open_jobs': num_open_jobs, 
                                                     'num_completed_jobs': num_completed_jobs,
                                                     'num_progress_jobs': num_progress_jobs})


        elif request.method == 'POST':
            user.profile.role = request.POST.get('inlineRadioOptions')
            user.profile.time_zone = request.POST.get('userTimezone')
            user.save()
            return redirect('home')
    return render(request, 'home.html', {"MissingInfo": False})
