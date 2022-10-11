from django.db import models

class Authentication(models.Model):

    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

class Profile(models.Model):

    name = models.CharField(max_length=100)
    house_no = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    isSeller = models.BooleanField(default=False)
    isBuyer = models.BooleanField(default=False)