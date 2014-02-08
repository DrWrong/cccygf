from django.conf.urls import patterns,url
from validate import views
urlpatterns = patterns('',
	url(r'^callback/$',views.callback,name='callback'),
	)