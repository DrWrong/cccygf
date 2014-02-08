from django.conf.urls import patterns,url
from validate import views
urlpatterns = patterns('',
	url(r'^sendmessage/$',views.smssend,name='smssend'),
	url(r'^callback/?P<sign>[^/]+/$',views.callback,name='callback'),
	)