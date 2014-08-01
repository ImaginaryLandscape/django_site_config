from django.views.generic.base import TemplateView
from site_config.utils import WebsiteOverrideTemplateViewMixin
from example.app_foo import FooConfig

class IndexView(WebsiteOverrideTemplateViewMixin, TemplateView):
    
    def dispatch(self, request, *args, **kwargs):
        self.website = kwargs.get('website', None)
        self.config = FooConfig(website=self.website)
        return super(IndexView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['config'] = self.config
        kwargs['website'] = self.website
        return kwargs
        