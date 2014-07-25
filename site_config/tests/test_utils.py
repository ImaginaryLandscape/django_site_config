from __future__ import unicode_literals
from django.test import TestCase
from django.test.utils import override_settings
from . import utils as test_utils
from site_config import utils


class SiteConfigMixin(object):

    def load_config(self):
        
        config_dict = {'TEST_A':{'default':
                                  "Test A default", 
                                  'field':'django.forms.CharField', 
                                  'help':'Test A help text.'}, 
                       "TEST_B":{'default':1, 
                                  'field':'django.forms.IntegerField', 
                                  'help':'Test B help text.'}} 
        self.config_dict = config_dict
        

@override_settings(**test_utils.settings_overrides)
class TestSiteConfigRegistry(SiteConfigMixin, TestCase):
    def setUp(self):
        self.load_config()
    
    def test_config_dict_value_from_default__default_equals_value(self):
        for k,v in utils.config_dict_value_from_default(self.config_dict).items():
            self.assertEqual(v['default'], v['value'], )

    def test_config_dict_value_from_default__default_equals_value(self):
        before = self.config_dict.keys()
        updated_config_dict = utils.config_dict_value_from_default(self.config_dict)
        after = self.config_dict.keys()
        self.assertListEqual(before, after,)
        
        self.assertEqual(updated_config_dict['TEST_A'].keys(), self.config_dict['TEST_A'].keys(), )