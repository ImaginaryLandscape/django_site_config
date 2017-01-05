from __future__ import unicode_literals

from .utils import import_module_attr


class ConfigRegistry():

    def __init__(self):
        self._registry = {}

    def register(self, siteconfig):
        self._registry[siteconfig.application_short_name] = (
            siteconfig.application_verbose_name, siteconfig)

    def get_config_list(self):
        return [(k, v[0]) for k, v in self._registry.items()]

    def get_config_class(self, application_short_name):
        return self._registry.get(application_short_name, None)


config_registry = ConfigRegistry()
