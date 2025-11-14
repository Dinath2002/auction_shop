# auctions/views.py

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Product, Bid
from .forms import ProductForm


def auction_list(request):
    """
    Show all active products (both Buy Now and Auctions).
    """
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "auctions/listing_list.html", {"products": products})


def auction_detail(request, pk):
    """
    Detail page for a single product (auction or buy-now).
    """
    product = get_object_or_404(Product, pk=pk)
    bids = product.bids.order_by("-amount", "-created_at") if product.is_auction else []

    context = {
        "product": product,
        "object": product,   # so your old template using {{ object }} still works
        "bids": bids,
    }
    return render(request, "auctions/listing_detail.html", context)


@login_required
def place_bid(request, pk):
    """
    Place a bid on an active auction.
    """
    product = get_object_or_404(
        Product,
        pk=pk,
        listing_type="BID",
        is_active=True,
    )

    if request.method == "POST":
        # read amount safely
        try:
            amount = Decimal(request.POST.get("amount", "0"))
        except Exception:
            messages.error(request, "Invalid bid amount.")
            return redirect("auctions:listing_detail", pk=product.pk)

        # minimum allowed = highest bid + min_increment (or starting_bid)
        min_allowed = product.starting_bid or Decimal("0")
        top = product.highest_bid
        if top is not None:
            min_allowed = top + (product.min_increment or Decimal("1.00"))

        # validate
        if product.auction_end and timezone.now() >= product.auction_end:
            messages.error(request, "This auction has ended.")
        elif amount < min_allowed:
            messages.error(
                request,
                f"Your bid must be at least {min_allowed}.",
            )
        else:
            Bid.objects.create(
                product=product,
                bidder=request.user,
                amount=amount,
            )
            messages.success(request, "Bid placed successfully!")

    return redirect("auctions:listing_detail", pk=product.pk)


@login_required
def buy_now(request, pk):
    """
    Simple 'buy now' flow for fixed-price products.
    For now, just mark the product as inactive and show a message.
    """
    product = get_object_or_404(
        Product,
        pk=pk,
        listing_type="BUY",
        is_active=True,
    )

    # here you’d normally create an order / payment etc.
    product.is_active = False
    product.save()

    messages.success(request, "You purchased this item (demo flow).")
    return redirect("auctions:listing_detail", pk=product.pk)


@login_required
def product_create(request):
    """
    Let a logged-in user create a product (sell item).
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user

            # clean up fields depending on type
            if product.listing_type == "BUY":
                product.starting_bid = None
                product.min_increment = None
                product.auction_end = None

            product.save()
            messages.success(request, "Product created successfully.")
            return redirect("auctions:listing_detail", pk=product.pk)
    else:
        form = ProductForm()

    return render(request, "auctions/product_form.html", {"form": form})


def product_status_json(request, pk):
    """
    Small JSON API for real-time status: current bid, time left, active flag.
    """
    product = get_object_or_404(Product, pk=pk)
    data = {
        "is_active": product.is_active,
        "is_auction": product.is_auction,
        "highest_bid": str(product.highest_bid) if product.highest_bid is not None else None,
        "time_left": product.time_left_seconds,
    }
    return JsonResponse(data)
