from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job
from .models import ReviewRating
from .models import Comment

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name','price', 'end_date', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'content')