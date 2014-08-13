# import mock
from copy import deepcopy
from django.test import TestCase
from django.test.utils import override_settings
# from site_config import settings as site_settings
from . import lib


settings = deepcopy(lib.settings_overrides)
settings.update(dict(
    SITECONFIG_BACKEND_DEFAULT="site_config.backends.settings_backend.SettingsBackend"),
    TEST_B='Result in B',
)


@override_settings(**settings)
class TestSettingsBackendBasicAccess(lib.SiteConfigMixin, TestCase):

    def setUp(self):
        self.load_config()
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)

    def test_attributeA_access(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(siteconfig.TEST_A, "Test A default")

    def test_attributeB_access(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(siteconfig.TEST_B, 'Result in B')

    def test_get_config_default_value_A(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(siteconfig.get_config("TEST_A")['value'],
                         self.config_dict['TEST_A']['default'])

    def test_get_config_has_proper_keys_A(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(self.config_dict["TEST_A"].keys() + ["value"],
                        siteconfig.get_config("TEST_A").keys(), )

    def test_get_config_has_proper_keys_B(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(self.config_dict["TEST_B"].keys() + ['value'],
                        siteconfig.get_config("TEST_B").keys(), )

    def test_get_config_default_value_B(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(siteconfig.get_config("TEST_B")['value'],
                         self.config_dict['TEST_B']['value'])


@override_settings(**settings)
class TestSettingsConfigActive(lib.SiteConfigMixin, TestCase):

    def _set_setting_active_state(self, application, webapp):
        self.Application.objects.filter().update(active=application)
        self.WebsiteApplication.objects.filter().update(active=webapp)

    def setUp(self):
        self.load_config()
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)
