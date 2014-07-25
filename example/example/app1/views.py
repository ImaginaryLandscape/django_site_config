from django.views.generic.base import TemplateView
from example.app1 import MyFunConfig

class IndexView(TemplateView):
    
    def get_context_data(self, **kwargs):
        config = MyFunConfig(website=None)
        kwargs['config'] = config
        return kwargs
        