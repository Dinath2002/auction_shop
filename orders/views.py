from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from cart.models import CartItem
from .models import Order, OrderItem

@login_required
@transaction.atomic
def checkout(request):
    items = list(CartItem.objects.select_related('product').filter(user=request.user))
    if not items:
        return render(request, 'orders/checkout.html', {'empty': True})
    total = sum(i.product.price * i.quantity for i in items)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total)
        for i in items:
            OrderItem.objects.create(order=order, product=i.product, quantity=i.quantity, price=i.product.price)
        CartItem.objects.filter(user=request.user).delete()
        return redirect('orders:order_success', order_id=order.id)
    return render(request, 'orders/checkout.html', {'items': items, 'total': total})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

# Create your views here.
