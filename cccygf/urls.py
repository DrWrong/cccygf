from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cccygf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/',include('store.urls',namespace="store")),
    url(r'^cart/',include('cart.urls',namespace='cart')),
    url(r'^user/',include('user.urls',namespace='user')),
    url(r'^verify/',include('validate.urls',namespace='validate'))
)
