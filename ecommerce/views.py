import json

from django import contrib
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Order, OrderItem, Customer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def productview(request , product_id , product_name):
    product = Product.objects.get(id=product_id , name=product_name )
    return render(request, 'store/productview.html', {'product': product})


def login_view(request, massages=None):
    if request.method == "POST":

        Customer.name = request.POST["username"]
        Customer.password = request.POST["password"]
        user = authenticate(request, username=Customer.name, password=Customer.password)
        if user is not None:
            login(request, user)
            return redirect('store')
    else:
        return render(request, 'store/login.html', {})


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/Store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/Cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # create Empty cart for now for none-logged in users
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/Checkout.html', context)


def updateItem(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)
