from django.conf.urls import patterns,url
from user import views

urlpatterns=patterns('',
	url(r'^register/$',views.register,name='register'),
	url(r'^register/mobile/$',views.register_mobile,name='mobile'),
	url(r'^register/email/$',views.register_email,name='email'),
	url(r'^active/?P<sign>[^/]*/?P<usernamehash>[^/]*/$',views.active_email,name='active'),
	url(r'^aggrement/$',views.useragreement,name='aggrement')
	)