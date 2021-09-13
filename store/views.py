from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cartData, guestOrder


# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context={'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context={'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context={'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def productDetail(request, id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(id=id)
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/productDetail.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(f'productId: {productId}, action: {action}')

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # Get the OrderItem from the Order, if created already then just update the quantity
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1  
    elif action == 'delete':
        orderItem.quantity = 0   
    orderItem.save()

    if orderItem.quantity < 1:
        orderItem.delete()
    

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.cart_total_price):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create( 
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
    
    return JsonResponse('Payment completed', safe=False)
