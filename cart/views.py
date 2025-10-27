from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from catalog.models import Product
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, 'cart/cart_detail.html', {'items': items, 'total': total})

@login_required
def remove_item(request, item_id):
    get_object_or_404(CartItem, id=item_id, user=request.user).delete()
    return redirect('cart:cart_detail')

# Create your views here.
