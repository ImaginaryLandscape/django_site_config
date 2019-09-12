from __future__ import absolute_import
from django.conf.urls import include, url
from site_config.decorators import enable_disable_website
from .views import IndexView

urlpatterns = [
   url(
       '^page3/$',
       'example.app_bar.views.index',
       {'template_name': 'app_bar/index.html'},
       name="app_bar_page3"),
   url(
       '^page2/$',
       'example.app_bar.views.index',
       {'template_name': 'app_bar/index.html'},
       name="app_bar_page2"),
   url(
       '^page1/$',
       IndexView.as_view(template_name='app_bar/index.html'),
       {},
       name="app_bar_page1"),
   url(
       '^$',
       IndexView.as_view(template_name='app_bar/index.html'),
       {},
       name="app_bar_index"),
]
