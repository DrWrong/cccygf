from store.models import Category
from store.untils import get_or_create_cart

def category(request):
	categ=Category.objects.all()
	return {'category':categ}
def cart(request):
	cart=get_or_create_cart(request)
	cart_item=cart.cartitem_set.all()
	return {'cart':cart,'cart_item':cart_item}

