from __future__ import unicode_literals
import os
from .utils import import_module_attr

settings = import_module_attr(
    os.getenv('SITECONFIG_SETTINGS_MODULE', 'django.conf.settings')
)

BACKEND = getattr(settings, 'SITECONFIG_BACKEND',
                  'site_config.backends.model_backend.DatabaseBackend')


class ConfigRegistry():

    def __init__(self):
        self._registry = {}

    def register(self, siteconfig):
        self._registry[siteconfig.application_slug] = (siteconfig.application_verbose_name, siteconfig)

    def get_config_list(self):
        return [ (k, v[0]) for k,v in self._registry.items() ]

    def get_config_class(self, application_slug):
        return self._registry.get(application_slug, None)


config_registry = ConfigRegistry()