from django.conf.urls import patterns, include, url
from site_config.decorators import enable_disable_website
from example.app_bar import BarConfig
from .views import IndexView

urlpatterns = [
   url('^$', enable_disable_website(IndexView.as_view(template_name='app_bar/index.html'), BarConfig), 
       {}, name="app_bar_index")
]
