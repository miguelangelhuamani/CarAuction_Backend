from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    locality = models.CharField(max_length=100, blank=True)
    municipality = models.CharField(max_length=100, blank=True)
