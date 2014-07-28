from django.views.generic.base import TemplateView
from example.app_bar import BarConfig

class IndexView(TemplateView):
    
    def get_context_data(self, **kwargs):
        website = kwargs.get('website', None)
        config = BarConfig(website=website)
        kwargs['config'] = config
        return kwargs
        