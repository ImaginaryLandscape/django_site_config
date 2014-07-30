from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from example.app_bar import BarConfig

class IndexView(TemplateView):
    
    def get_context_data(self, **kwargs):
        website = kwargs.get('website', None)
        config = BarConfig(website=website)
        kwargs['config'] = config
        return kwargs

def index(request, template_name, website=None, *args, **kwargs):
    config = BarConfig(website=website)
    return render_to_response(template_name,
                              {'config':config,},
                              context_instance=RequestContext(request))
    
    