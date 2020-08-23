from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from . models import *


def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {
		    'get_cart_total':0, 'get_cart_items':0,'shipping':False
		}
		cartItems = order['get_cart_items']
	products = product.objects.all()
	context = {'products': products,'cartItems':cartItems,}
	return render(request, 'store/store.html',context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {
		    'get_cart_total':0, 'get_cart_items':0,'shipping':False
		}
		cartItems = order['get_cart_items']
	context={'items':items ,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {
		    'get_cart_total':0, 'get_cart_items':0,'shipping':False
		}
		cartItems = order['get_cart_items']
	context={'items':items ,'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html',context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('action',action)
	print('productId',productId)

	customer = request.user.customer
	Product= product.objects.get(id=productId)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)
	orderitem,created=orderItem.objects.get_or_create(order=order,product=Product)

	if action =='add':
		orderitem.quantity = (orderitem.quantity + 1)
	elif action =='remove':
		orderitem.quantity = (orderitem.quantity - 1)

	orderitem.save()

	if orderitem.quantity <= 0:
		orderitem.delete()
	return JsonResponse('Item was added',safe=False)

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete =True
		order.save()

		if order.shipping == True:
			shippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
				country=data['shipping']['country'],

				)

	else:
		print('User is not logged in')
	return JsonResponse('Payment Complete',safe=False)
# Create your views here.
