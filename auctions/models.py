from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from catalog.models import Product

class Listing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='listings')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    is_closed = models.BooleanField(default=False)

    def current_bid(self):
        top = self.bids.order_by('-amount').first()
        return top.amount if top else self.starting_price

    def __str__(self): return f"{self.product.title} auction"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount', '-placed_at']

# Create your models here.
