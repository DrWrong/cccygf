from django.conf.urls import patterns,url
from cart import views

urlpatterns=patterns('',
	url(r'^inline/$',views.inlinecart,name='inlinecart'),
	)