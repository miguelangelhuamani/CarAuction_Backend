from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator




class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    locality = models.CharField(max_length=100, blank=True)
    municipality = models.CharField(max_length=100, blank=True)

class UserWallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    card_number = models.CharField(max_length=19, validators=[
        MinLengthValidator(13),
        MaxLengthValidator(19)
    ])
    balance = models.DecimalField(max_digits = 10, default=0, decimal_places=2,
                                  validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.balance)