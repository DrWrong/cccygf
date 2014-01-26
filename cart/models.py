from django.db import models
from store.exception_define import NotEnoughProduct,ProductOffline
from django.contrib.auth.models import User
from store.models import ProductsGroup,Products
# Create your models here.
class Cart(models.Model):
	user=models.OneToOneField(User,blank=True,null=True)
	session=models.CharField(blank=True,max_length=100,unique=True)
	creation_date=models.DateTimeField(auto_now_add=True)
	modification_date=models.DateTimeField(auto_now=True,auto_now_add=True)

	def add_or_modify(self,product,amount=1):
		try:
			cart_item=CartItem.objects.get(cart=self,product=product)
		except CartItem.DoesNotExist:
			cart_item=CartItem.objects.create(cart=self,product=product,amount=amount)
		else:
			cart_item.amount+=amount

		cart_item.save()
		return cart_item
	def get_items(self):
		return CartItem.objects.select_related()\
		.filter(cart=self,product__active=True)




class CartItem(models.Model):
	"""docstring for CartItem"""
		
	cart=models.ForeignKey(Cart)
	product=models.ForeignKey(Products)
	amount=models.PostiveSmallIntegerField(blank=True,null=True)
	creation_date=models.DateTimeField(auto_now_add=True)
	modification_date=models.DateTimeField(auto_now=True,auto_now_add=True)
	def get_price(self,request):
		if self.product.ProductsGroup.issale:
			return self.product.ProductsGroup.saleprice
		if request.user.is_authenticated():
			if request.user.userinfo.vip:
				return self.product.ProductsGroup.vipprice
		return self.product.ProductsGroup.price
	def get_price_gross(self,request):
		price=self.get_price(request)
		return price*self.amount

	def save(self,*args,**kwargs):
		if self.amount>self.product.amount:
			raise NotEnoughProduct('product not enough')
		if self.product.active==False:
			raise ProductOffline('product off line')