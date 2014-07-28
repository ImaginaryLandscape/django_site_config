from __future__ import unicode_literals
import mock
from copy import deepcopy
from django.test import TestCase
from django.test.utils import override_settings
from site_config import utils
from . import lib
   

settings = deepcopy(lib.settings_overrides)
settings.update(dict(SITECONFIG_BACKEND="site_config.backends.settings_backend.SettingsBackend"))

@override_settings(**settings)
class TestSiteConfigRegistry(lib.SiteConfigMixin, TestCase):
    def setUp(self):
        self.load_config()

    def test_register_site_config(self):
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)
        self.assertIsNotNone(self.site_config.registry.config_registry.get_config_class('myapp'), )

    def test_register_site_config_verbose_name(self):
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)
        self.assertEqual(self.site_config.registry.config_registry.get_config_class('myapp')[0],
                         self.MyAppSiteConfig.application_verbose_name)

    def test_register_site_config_short_name(self):
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)
        config_class = self.site_config.registry.config_registry.get_config_class('myapp')[1]
        self.assertEqual(config_class.application_short_name,
                         self.MyAppSiteConfig.application_short_name)

