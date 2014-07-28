from django.conf.urls import patterns, include, url
from site_config.decorators import determine_website
from example.app_foo import FooConfig
from .views import IndexView

urlpatterns = [
   url('^$', determine_website(IndexView.as_view(template_name='app_foo/index.html'), FooConfig), 
       {}, name="app_foo_index")
]
