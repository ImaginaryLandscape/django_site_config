from django.conf.urls import patterns, include, url
from site_config.decorators import determine_website
from .views import IndexView

urlpatterns = [
   url('^$', determine_website(IndexView.as_view(template_name='app_bar/index.html')), 
       {}, name="app_bar_index")
]
