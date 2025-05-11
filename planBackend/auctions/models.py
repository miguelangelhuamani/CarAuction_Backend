from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.exceptions import ValidationError
from django.utils.timezone import now

from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.name

class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    closing_date = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='auctions/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, related_name='auctions',on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)

    auctioneer = models.ForeignKey(CustomUser, related_name='auctions',on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering=('id',)

    def __str__(self):
        return self.title

class Rating(models.Model):
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    auction = models.ForeignKey(Auction, related_name="ratings", on_delete=models.CASCADE)
    rater = models.ForeignKey(CustomUser, related_name="ratings", on_delete=models.CASCADE)

    class Meta:
        ordering = ("rating",)
        constraints = [
            models.UniqueConstraint(fields=["auction", "rater"], name="unique_rating_per_user")
        ]

    def __str__(self):
        return str(self.rating)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-amount',)

    def __str__(self):
        return str(self.amount)
    


class Comment(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"