from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(template_name='index.html'), {}, name="index"),                       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<website>\w+)/foo/$', include('example.app_foo.urls')),
    url(r'^(?P<website>\w+)/bar/$', include('example.app_bar.urls')),
)

