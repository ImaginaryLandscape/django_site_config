from __future__ import absolute_import
from django.conf.urls import include, url
from site_config.decorators import enable_disable_website
from .views import IndexView

urlpatterns = [
   url('^$', IndexView.as_view(template_name='app_foo/index.html'), {}, name="app_foo_index")
]
