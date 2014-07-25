from __future__ import unicode_literals
from django.test import TestCase
from django.test.utils import override_settings
from . import utils as test_utils
from site_config import utils


class SiteConfigMixin(object):

    def load_config(self):
        
        config_dict = {'TEST_A':{'default':"Test A default", 
                                 'field':'django.forms.CharField', 
                                 'help':'Test A help text.'},
                       "TEST_B":{'default':1,
                                 'field':'django.forms.IntegerField', 
                                 'help':'Test B help text.'},
                       }
        self.config_dict = config_dict
        

@override_settings(**test_utils.settings_overrides)
class TestSiteConfigRegistry(SiteConfigMixin, TestCase):
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
        