import mock
from copy import deepcopy
from django.test import TestCase
from django.test.utils import override_settings
from site_config import settings as site_settings
from . import utils
   

settings = deepcopy(utils.settings_overrides)
settings.update(dict(
    SITECONFIG_BACKEND="site_config.backends.settings_backend.SettingsBackend"),
    TEST_B='Result in B',
)


@override_settings(**settings)
class TestSettingsBackendBasicAccess(utils.SiteConfigMixin, TestCase):
    
    def setUp(self):
        self.old_setting = site_settings.BACKEND
        site_settings.BACKEND = "site_config.backends.settings_backend.SettingsBackend"
        self.load_config()
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)

    def tearDown(self):
       site_settings.BACKEND = self.old_setting

    def test_attributeA_access(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(siteconfig.TEST_A, "Test A default")

    def test_attributeB_access(self):
        siteconfig = self.MyAppSiteConfig(website=None)
        self.assertEqual(siteconfig.TEST_B, 'Result in B')

