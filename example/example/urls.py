from __future__ import absolute_import
from django.conf.urls import include, url
from django.contrib import admin
from site_config.decorators import enable_disable_website, website_template_override, decorated_includes
from example.app_foo import FooConfig
from example.app_bar import BarConfig
from . import views

admin.autodiscover()


urlpatterns = [
    url(r'^$', views.HomeView.as_view(template_name='index.html'), {}, name="index"),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += decorated_includes(
    lambda func: enable_disable_website(func, FooConfig),
    [url(r'^(?P<website>\w+)/foo/', include('example.app_foo.urls'))],
)

urlpatterns += decorated_includes(
    lambda func: enable_disable_website(func, BarConfig),
    [url(r'^(?P<website>\w+)/bar/', include('example.app_bar.urls'))],
)
