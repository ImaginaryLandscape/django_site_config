from django.views.generic.base import TemplateView
from example.app_foo import FooConfig

class IndexView(TemplateView):
    
    def get_context_data(self, **kwargs):
        website = kwargs.get('website', None)
        config = FooConfig(website=website)
        kwargs['config'] = config
        return kwargs
        