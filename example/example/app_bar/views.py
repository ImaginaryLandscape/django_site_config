from __future__ import absolute_import
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from site_config.utils import WebsiteOverrideTemplateViewMixin
from site_config.decorators import website_template_override
from example.app_bar import BarConfig


class IndexView(WebsiteOverrideTemplateViewMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        self.website = kwargs.get('website', None)
        self.config = BarConfig(website=self.website)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['config'] = self.config
        kwargs['website'] = self.website
        return kwargs


@website_template_override
def index(request, template_name, website=None, *args, **kwargs):
    config = BarConfig(website=website)
    return render_to_response(template_name,
                              {
                               'website': website,
                               'config': config,
                               'template_name': template_name,
                               },
                              context_instance=RequestContext(request))
