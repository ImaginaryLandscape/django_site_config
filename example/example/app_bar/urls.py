from django.conf.urls import patterns, include, url
from site_config.decorators import enable_disable_website
from .views import IndexView

urlpatterns = [
   url('^page2/$', IndexView.as_view(template_name='app_bar/index.html'), {}, name="app_bar_page2"),  
   url('^page1/$', IndexView.as_view(template_name='app_bar/index.html'), {}, name="app_bar_page1"),   
   url('^$', IndexView.as_view(template_name='app_bar/index.html'), {}, name="app_bar_index"),
]
