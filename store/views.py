from django.shortcuts import render,get_object_or_404
from store.models import ProductsGroup,Category,Products
from django.http import HttpResponse
from cms.models import Gallery
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def home(request):
	newProduct=ProductsGroup.objects.filter(active=True).order_by('-pub_time')[:9]
	hotProduct=ProductsGroup.objects.filter(active=True).order_by('salenumber')[:10]
	mostCommentproduct=ProductsGroup.objects.filter(active=True)\
	.order_by('commentnumber')[:7]
	saleProduct=ProductsGroup.objects.filter(active=True).filter(issale=True)
	gallery=Gallery.objects.all()
	return render(request,'store/home.html',{'newProduct':newProduct,\
		'hotProduct':hotProduct,'mostCommentproduct':mostCommentproduct,\
		'saleProduct':saleProduct,'showgallery':gallery})

#TODO 查询功能优化
def search(request):
	q=request.GET.get("q",'')
	if q=='':
		status=2
		product=ProductsGroup.objects.filter(active=True).all()
	else:
		query=Q(active=True)&(Q(name__icontains=q)|Q(merchant__name__icontains=q))
		product=ProductsGroup.objects.filter(query)
		total=len(product)
		if total==0:
			status=1
			product=ProductsGroup.objects.filter(active=True).order_by('salenumber')[:5]
		else:
			status=0
	return _displaycategory(request,status,product,total)

def category(request,cid):
	products=ProductsGroup.objects.filter(active=True).filter(category__id=cid)
	fid=request.GET.get("fid",'')
	if fid!='':
		filteridlist=fid.split('+')
		for filterid in filteridlist:
			try:		
				fid=int(filterid)
			except:
				return HttpResponse(status="400")
			try:
				products=products.filter(filterchoice_set__id=fid)
			except:
				return HttpResponse(status="400")

	sortid=request.GET.get("sortid",'')
	if sortid!='':
		try:
			sortid=int(sortid)
		except:
			return HttpResponse(status="400")
		if sortid not in list(range(4)):
			return HttpResponse(status="400")

		sort=request.GET.get("sort",'')
		if sortid!='':
			sort=int(sort)
			if sort not in [0,1]:
				return HttpResponse(status='400')
			sortlist=['default','pub_time','price','hitnumber']
			if sortid!=0:
				order=sortlist[sortid]
				if sort==0:
					order='-'+order
				products=products.order_by(order)
			if products.count()==0:
				status=1
			else:
				status=0
			return _displaycategory(request,status,products)
		return HttpResponse(status='400')

def _displaycategory(request,status,products=None,total=0):
	if status!=1:
		filterdict={}
		for product in products:
			filters=product.filterchoice_set.all()
			for eachfilter in filters:
				if eachfilter.name not in filterdict:
					filterdict[eachfilter.name]=\
					[{'fid':eachfilter.id,'vaule':eachfilter.value},]
				else:
					newdict={'fid':eachfilter.id,'value':eachfilter.value}
					if newdict not in filterdict[eachfilter.name]:
						filterdict[eachfilter.name].append(newdict)
	return render(request,'store/category.html',\
		{'status':status,'filters':filterdict,'products':product,'total':total})


def detail(request,pid):
	product=get_object_or_404(Products,id=pid)
	productgroup=product.productgroup
	if productgroup.active==False:
		status=3#商品已下线
		return render(request,'store/detail.html',{'status':status})
	productgroup.hitnumber+=1
	productgroup.save()
	recpid=productgroup.recommandproducts_set.values_list('recpid',flat=True)
	if len(recpid)!=0:
		products=[]
		for pid in recpid:
			try:
				product=ProductsGroup.objects.get(id=pid)
			except ObjectDoesNotExist:
				pass
			if product.active:
				products.append(product)
	return render(request,'store/detail.html',{'product':product,'recommand':products})	

def cart(request):
	try:
		category=Category.objects.get(small_prodcut=True)
		productgroups=category.productsgroup_set.all()[:5]
	except:
		productgroups=[]
	return render(request,'store/cart.html',{'recommands':productgroups})
		



