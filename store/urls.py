from django.conf.urls import patterns,url

from store import views 

urlpatterns=patterns('',
	
	url(r'^home$',views.home,name='index'),
	url(r'^search$',views.search,name='search'),
	url(r'^category/(?P<cid>\d+)$',views.category,name='category'),
	url(r'^item/(?P<pid>\d+)$',views.detail,name='detail'),
	url(r'^cart/$',views.cart,name='cart')
	)

