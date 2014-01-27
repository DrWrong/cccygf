from store.models import Category

def category(request):
	categ=Category.objects.all()
	return {'category':categ}


