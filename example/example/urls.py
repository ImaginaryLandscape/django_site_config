from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), {}, name="index"),                       
    url(r'^app1/$', include('example.app1.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

