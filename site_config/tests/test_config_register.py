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
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        self.assertIsNotNone(self.site_config.settings.config_registry.get_config_class('myapp'), )

    def test_register_site_config_verbose_name(self):
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        self.assertEqual(self.site_config.settings.config_registry.get_config_class('myapp')[0],
                         self.MyAppSiteConfig.application_verbose_name)

    def test_register_site_config_short_name(self):
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        config_class = self.site_config.settings.config_registry.get_config_class('myapp')[1]
        self.assertEqual(config_class.application_short_name,
                         self.MyAppSiteConfig.application_short_name)
    
    def test_get_settings_backend(self):
        self.assertEqual(self.site_config.settings.BACKEND,
                         lib.settings_overrides['SITECONFIG_BACKEND'])


@override_settings(**lib.settings_overrides)
class TestSiteConfigRegistry2(lib.SiteConfigMixin, TestCase):
    def setUp(self):
        self.load_config()

    def test_config_dict_value_from_default__value_key_added(self):
        self.assertNotIn("value", self.config_dict['TEST_A'])
        self.assertNotIn("value", self.config_dict['TEST_B'])
        updated_config_dict = utils.config_dict_value_from_default(self.config_dict)
        self.assertIn("value", updated_config_dict['TEST_A'])
        self.assertIn("value", updated_config_dict['TEST_B']) 
        self.assertNotIn("value", self.config_dict['TEST_A'])
        self.assertNotIn("value", self.config_dict['TEST_B'])

    def test_config_dict_value_from_default__default_equals_value(self):
        for k,v in utils.config_dict_value_from_default(self.config_dict).items():
            self.assertEqual(v['default'], v['value'], )

    def test_update_config_dict__single_update(self):
        updated_config_dict = {'TEST_A': {"value": "5432"},
                               }
        updated = utils.update_config_dict(self.config_dict, updated_config_dict)
        self.assertEqual(updated["TEST_A"]["value"], "5432", )
        self.assertFalse(updated["TEST_B"].has_key("value"))

    def test_update_config_dict__all_update(self):
        updated_config_dict = {'TEST_A': {"value": "5432"},
                               'TEST_B': {"value": 2},
                               }
        updated = utils.update_config_dict(self.config_dict, updated_config_dict)
        self.assertEqual(updated["TEST_A"]["value"], "5432", )
        self.assertEqual(updated["TEST_B"]["value"], 2, )

    def test_update_config_dict__extra_update(self):
        updated_config_dict = {'TEST_A': {"value": "5432"},
                               'TEST_C': {"value": 2},
                               }
        updated = utils.update_config_dict(self.config_dict, updated_config_dict)
        self.assertEqual(updated["TEST_A"]["value"], "5432", )
        self.assertTrue(updated.has_key("TEST_B"))
        self.assertFalse(updated.has_key('TEST_C'))