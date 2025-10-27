from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Listing, Bid

class ListingListView(ListView):
    model = Listing
    template_name = 'auctions/listing_list.html'

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'auctions/listing_detail.html'

@login_required
def place_bid(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_closed=False)
    if listing.ends_at <= timezone.now():
        listing.is_closed = True
        listing.save(update_fields=['is_closed'])
        messages.error(request, 'Auction ended')
        return redirect('auctions:listing_detail', pk=pk)

    amount = request.POST.get('amount')
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        messages.error(request, 'Invalid bid')
        return redirect('auctions:listing_detail', pk=pk)

    current = float(listing.current_bid())
    if amount <= current:
        messages.error(request, f'Your bid must be higher than current bid (Rs. {current})')
        return redirect('auctions:listing_detail', pk=pk)

    Bid.objects.create(listing=listing, bidder=request.user, amount=amount)
    messages.success(request, 'Bid placed!')
    return redirect('auctions:listing_detail', pk=pk)

@login_required
def buy_now(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_closed=False)
    if listing.buy_now_price:
        listing.is_closed = True
        listing.save(update_fields=['is_closed'])
        messages.success(request, 'Purchased via Buy Now!')
    else:
        messages.error(request, 'Buy Now not available')
    return redirect('auctions:listing_detail', pk=pk)

# Create your views here.
