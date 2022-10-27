from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    time_zone = models.CharField(max_length=500, default=timezone.now())
    native_auth = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'


class Job(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    description = models.TextField()
    url2audio = models.TextField()
    worker_id = models.CharField(max_length=100)
    status_choices = [  # 0 = not started, 1 = in progress, 2 = completed, 3 = cancelled
        (0, 'CLAIMED'),
        (1, 'INPROGRESS'),
        (2, 'COMPLETED'),
        (3, 'CANCELLED')
    ]
    status = models.IntegerField(choices=status_choices, default=0)
