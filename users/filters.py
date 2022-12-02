import django_filters
from .models import *
from django import forms
from django.forms import MultiWidget

class JobFilter(django_filters.FilterSet):
    #created_date = django_filters.DateFilter(field_name='created_date', label='Created Date', widget=forms.DateInput())
    created_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'placeholder':'mm-dd-yyyy',
                                                                           'class':'form-control', 
                                                                           'type':'date',
                                                                           'style':'margin-bottom: 1rem;font-size: 15px;font-family: POPPINS;padding-right: 10px;font-weight: 400;width: 75%;margin-left: 10px;'}),
                                                                            lookup_expr='icontains')
    end_date = django_filters.DateFilter(widget=forms.DateInput(attrs={'placeholder':'mm-dd-yyyy',
                                                                       'class':'form-control', 
                                                                       'type':'date',
                                                                       'style':'margin-bottom: 1rem;font-size: 15px;font-family: POPPINS;padding-right: 10px;font-weight: 400;width: 75%;margin-left: 10px;'}), 
                                                                       lookup_expr='icontains')
    price = django_filters.RangeFilter(widget=MultiWidget(widgets=[forms.NumberInput(attrs={'class':'form-control',
                                                                                            'placeholder':'MIN',
                                                                                            'style':'width: 30%;margin-left: 1px;font-size: 15px;font-family: POPPINS;'}),
                                                                   forms.NumberInput(attrs={'class':'form-control',
                                                                                            'placeholder':'MAX',
                                                                                            'style':'width: 30%;margin-left: 40px;font-size: 15px;font-family: POPPINS;'})]))
    class Meta:
        model= Job
        fields = {
            'status',
            'created_date',
            'end_date',
            'price',
        }

