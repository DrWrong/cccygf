from cart.models import Cart
from django.core.exceptions import ObjectDoesNotExist

def get_or_create_cart(request):
	cart=get_cart(request)
	if cart is None:
		cart=create_cart(request)
def create_cart(request):
	if request.session.session_key is None:
		request.session.save()
	cart=Cart(session=request.session.session_key)
	if request.user.is_authenticated():
		cart.user=request.user
	
	cart.save()
	return cart

def get_cart(request):
	session_key=request.session.session_key
	user=request.user
	if user.is_authenticated():
		try:
			cart=Cart.objects.get(user=user)
			return cart
		except ObjectDoesNotExist:
			return None
	else:
		try:
			cart=Cart.objects.get(session=session_key)
			return cart
		except ObjectDoesNotExist:
			return None
def update_cart_after_login(request):
	try:
		session_cart=Cart.objects.get(session=request.session.session_key)
		try:
			user_cart=Cart.objects.get(user=request.user)
		except ObjectDoesNotExist:
			session_cart.user=request.user
			session_cart.save()
		else:
			for session_cart_item in session_cart.get_items():
				user_cart.add(session_cart_item.product,session_cart_item.amount)
			session_cart.delete()
	except ObjectDoesNotExist:
		pass
