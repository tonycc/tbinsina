from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tbinsina/', include('tbinsina.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'tbinsina.weibo.views.index',name=""),
    url(r'^index/$','tbinsina.weibo.views.index',name='index'),
    url(r'^login/$','tbinsina.weibo.views.login',name='login'),
    url(r'^login_check/$','tbinsina.weibo.views.login_check',name="logincheck"),
    url(r'^getfans/$','tbinsina.weibo.views.get_fans',name="getfans"),
    url(r'^comments/$','tbinsina.weibo.views.comments',name="getfans"),
)
