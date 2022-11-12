from django.shortcuts import render
from django.contrib.auth.models import User
import pytz

def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
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

        elif request.method == 'POST':
            user.profile.role = request.POST.get('inlineRadioOptions')
            user.profile.time_zone = request.POST.get('userTimezone')
            user.save()

            render(request, 'home.html', {"MissingInfo": False})

    return render(request, 'home.html', {"MissingInfo": False})
