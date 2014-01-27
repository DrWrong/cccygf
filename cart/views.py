from django.shortcuts import render
from cart.untils import get_or_create_cart
from django.core import serializers
from django.HttpResponse
import json
from cccygf.exception_define import ProductUnbought
from django.core.exceptions import  NotEnoughProduct,ProductOffline,ProductUnbought

from store.modles import Products

# Create your views here.

def inlinecart(request):
	cart=get_or_create_cart(request)
	if request.method="POST":
		req=json.loads(request.body)
		pid=req['pid']
		status=0
		error=''
		if req['operator']==0:
			try:
				cart.delete_item(pid)
			except ProductUnbought:
				status=5
				error='所要删除商品尚未购买'
		elif req['operator']==1:
			try:
				product=Products.object.get(id=pid)
			except ObjectDoesNotExist:
				status=1
				error='没有所需要商品'
			else:
				try:
					cart.add_or_modify(product)
				except ProductOffline:
					status=3
					error='商品已下线'
				except NotEnoughProduct:
					status=6
					error='商品缺货'
	
	cart_items=cart.cartitem_set.all()
	data={}
	if len(cart_item)==0:
		status=4
		error='购物车里没有商品'
	else:
		values=[]
		for item in cart_items:
			values.append({'imgurl':item.product.sketch,
				'name':item.product.name,
				'price':item.get_price(),
				'amount':item.amount,
				'pid':item.productid})

		data['value']=values
	data['status']=status
	data['error']=error
	
	return HttpResponse(json.dumps(data,ensure_ascii=False),content_type='application/json')

