from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name

#Validación personalizada (DUDA)
def validate_closing_date(value):
    """ Valida que la fecha de cierre sea al menos 15 días después de la fecha de creación """
    min_date = now() + timedelta(days=15)
    if value < min_date:
        raise ValidationError(f"La fecha de cierre debe ser al menos 15 días después de hoy ({min_date.date()}).")

class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    closing_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='auctions/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    category = models.ForeignKey(Category, related_name='auctions',on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return self.amount

