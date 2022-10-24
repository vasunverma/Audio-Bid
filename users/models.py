from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    time_zone = models.CharField(max_length=500)
    native_auth = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
