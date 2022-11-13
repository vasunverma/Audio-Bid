import django_filters

from .models import *

class JobFilter(django_filters.FilterSet):
    class Meta:
        model= Job
        fields = ['status']

