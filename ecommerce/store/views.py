from django.shortcuts import render
from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    context={'products': products}
    return render(request, 'store/store.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Get all the "orderitem" that has the foreign key of the "order"
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'cart_total_items':0, 'cart_total_price':0}
    context={'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # Get all the "orderitem" that has the foreign key of the "order"
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'cart_total_items':0, 'cart_total_price':0}
    context={'items': items, 'order': order}
    return render(request, 'store/cart.html', context)
