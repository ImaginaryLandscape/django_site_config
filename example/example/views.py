from django.views.generic.base import TemplateView
from example.app_bar import BarConfig
from site_config.backends.model_backend import models


class HomeView(TemplateView):

    def get_context_data(self, **kwargs):
        kwargs['websites'] = models.Website.objects.all()
        return kwargs
