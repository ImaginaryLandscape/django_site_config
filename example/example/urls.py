from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), {}, name="index"),                       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<website>\w+)/foo/$', include('example.app_foo.urls')),
    url(r'^(?P<website>\w+)/bar/$', include('example.app_bar.urls')),
)

