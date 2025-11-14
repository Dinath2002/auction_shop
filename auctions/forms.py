# auctions/forms.py
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    # nicer datetime widget for auction end
    auction_end = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "image",
            "listing_type",
            "price",
            "starting_bid",
            "min_increment",
            "auction_end",
            "is_active",
        ]

    def clean(self):
        cleaned = super().clean()
        listing_type = cleaned.get("listing_type")
        starting_bid = cleaned.get("starting_bid")
        auction_end = cleaned.get("auction_end")

        # extra validation for auctions
        if listing_type == "BID":
            if not starting_bid:
                self.add_error("starting_bid", "Starting bid is required for auctions.")
            if not auction_end:
                self.add_error("auction_end", "Auction end time is required for auctions.")

        return cleaned
