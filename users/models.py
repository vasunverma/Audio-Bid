from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    time_zone = models.CharField(max_length=500)
    native_auth = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    number_of_ratings = models.IntegerField(default='0')

    def __str__(self):
        return f'{self.user.username} Profile'

class Job(models.Model):
    name= models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    limit_price = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    claim_date = models.DateTimeField(null=True)
    description = models.TextField()
    url2audio = models.TextField()
    url2Transcript = models.TextField(null=True)
    worker_id = models.CharField(max_length=100, default='0')
    status_choices = [  # 0 = not started, 1 = in progress, 2 = completed, 3 = cancelled
        (0, 'AVAILABLE'),
        (1, 'INPROGRESS'),
        (2, 'COMPLETED'),
        (3, 'INREVIEW')
    ]
    status = models.IntegerField(choices=status_choices, default=0)


class ReviewRating(models.Model):
    job_id = models.BigIntegerField(default='-1')
    creator_id = models.CharField(max_length=100, default='0')
    worker_id = models.CharField(max_length=100, default='0')
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class Comment(models.Model):
    name = models.CharField(max_length=50, blank=True)
    content = models.TextField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)