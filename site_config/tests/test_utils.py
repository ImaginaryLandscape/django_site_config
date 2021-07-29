import mock
from copy import deepcopy
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings
from site_config import utils
from . import lib


@override_settings(**lib.settings_overrides)
class TestUtils(lib.SiteConfigMixin, TestCase):
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
        for k, v in utils.config_dict_value_from_default(self.config_dict).items():
            self.assertEqual(v['default'], v['value'], )

    def test_update_config_dict__single_update(self):
        updated_config_dict = {'TEST_A': {"value": "5432"},
                               }
        updated = utils.update_config_dict(self.config_dict, updated_config_dict)
        self.assertEqual(updated["TEST_A"]["value"], "5432", )
        self.assertFalse("value" in updated["TEST_B"])

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
        self.assertTrue("TEST_B" in updated)
        self.assertFalse('TEST_C' in updated)

    @mock.patch('site_config.utils.select_template')
    def test_website_override_tamplate__exist(self, select_template):
        select_template.return_value = 'Joe/app1'
        self.assertEqual('Joe/app1',
            utils.website_override_template('Joe', 'app1')
                         )

    @mock.patch('site_config.utils.select_template')
    def test_website_override_tamplate__unexist(self, select_template):
        select_template.return_value = 'app1'
        self.assertEqual('app1',
            utils.website_override_template('Joe', 'app1')
                         )

    class baseObj(object):
        def __init__(self):
            self.template_name = 'app.html'
            self.website = 'Example'
            self.kwargs = {}

        def get_template_names(self):
            # Direct implementation from TemplateResponseMixin
            if self.template_name is None:
                raise ImproperlyConfigured(
                    "TemplateResponseMixin requires either a definition of "
                    "'template_name' or an implementation of "
                    "'get_template_names()'"
                )
            else:
                return [self.template_name]

    class testObj(utils.WebsiteOverrideTemplateViewMixin, baseObj):
        pass

    def test_website_override_template_view_mixin_website_set(self):
        test_obj = self.testObj()
        self.assertEqual(
            set(test_obj.get_template_names()),
            set(['Example/app.html', 'app.html'])
        )

    def test_website_override_template_view_mixin_website_set_kwargs_set(self):
        test_obj = self.testObj()
        test_obj.kwargs['website'] = 'Dan'
        self.assertEqual(
            set(test_obj.get_template_names()),
            set(['Example/app.html', 'app.html'])
        )

    def test_website_override_template_view_mixin_no_website_no_kwargs(self):
        test_obj = self.testObj()
        test_obj.website = None
        self.assertEqual(
            set(test_obj.get_template_names()),
            set(['app.html'])
        )

    def test_website_override_template_view_mixin_no_website_set_kwargs(self):
        test_obj = self.testObj()
        test_obj.website = None
        test_obj.kwargs['website'] = 'Different'
        self.assertEqual(
            set(test_obj.get_template_names()),
            set(['Different/app.html','app.html'])
        )

