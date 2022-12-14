from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job
from .models import ReviewRating
from .models import Comment

# JobForm is used to create a job
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['name','price', 'end_date', 'description', 'limit_price']

# Review form is used to create a review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']

# Comment form is used to create a comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'content')