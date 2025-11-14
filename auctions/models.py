# auctions/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    LISTING_TYPE_CHOICES = [
        ("BUY", "Buy Now"),
        ("BID", "Auction (Bidding)"),
    ]

    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    listing_type = models.CharField(
        max_length=3,
        choices=LISTING_TYPE_CHOICES,
        default="BUY",
    )

    # BUY NOW price (also used as reference for auction if needed)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Buy Now price"
    )

    # Auction-only fields
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    min_increment = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        help_text="Minimum amount above current bid"
    )
    auction_end = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_auction(self):
        return self.listing_type == "BID"

    @property
    def highest_bid(self):
        if not self.is_auction:
            return None
        top = self.bids.order_by("-amount").first()
        return top.amount if top else self.starting_bid

    @property
    def time_left_seconds(self):
        if not self.auction_end:
            return None
        delta = self.auction_end - timezone.now()
        return max(int(delta.total_seconds()), 0)


class Bid(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="bids"
    )
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} -> {self.product} ({self.amount})"
