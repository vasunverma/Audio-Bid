import django_filters
from .models import *
from django import forms

class JobFilter(django_filters.FilterSet):
    #created_date = django_filters.DateFilter(field_name='created_date', label='Created Date', widget=forms.DateInput())
    created_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}), lookup_expr='icontains')
    end_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}), lookup_expr='icontains')
    price = django_filters.RangeFilter()
    class Meta:
        model= Job
        fields = {
            'status',
            'created_date',
            'end_date',
            'price',
        }

