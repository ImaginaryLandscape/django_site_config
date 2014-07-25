from django.conf.urls import patterns, include, url
from .views import IndexView

urlpatterns = [
   url('^$', IndexView.as_view(template_name='app1/index.html'), {},
       name="app1_index")
]
