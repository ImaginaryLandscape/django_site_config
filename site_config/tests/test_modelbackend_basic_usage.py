# import mock
from copy import deepcopy
from django.test import TestCase
from django.test.utils import override_settings
from . import lib


class ModelsBaiscMixin(object):

    def load_models(self):
        self.Website = self.site_config.backends.model_backend.models.Website
        self.Application = self.site_config.backends.model_backend.models.Application
        self.WebsiteApplication = self.site_config.backends.model_backend.models.WebsiteApplication

        self.sites = []
        self.site1_short_name = "joe"
        site = self.Website(
            name="JOE SITE", short_name=self.site1_short_name,
            active=True)
        site.save()
        self.sites.append(site)

        self.site2_short_name = "john"
        site = self.Website(
            name="John Site", short_name=self.site2_short_name,
            active=False)
        site.save()
        self.sites.append(site)

        self.apps = []
        self.app1_short_name = 'myapp'
        app = self.Application(short_name=self.app1_short_name, active=True)
        app.save()
        self.apps.append(app)

        webapp = self.WebsiteApplication(
            website=self.sites[0], application=self.apps[0],
            active="enabled")
        webapp.save()
        self.webapps = []
        self.webapps.append(webapp)


settings = deepcopy(lib.settings_overrides)
settings.update(dict(SITECONFIG_BACKEND_DEFAULT="site_config.backends.model_backend.DatabaseBackend"))


@override_settings(**settings)
class TestModelBackendBasicAccess(ModelsBaiscMixin, lib.SiteConfigMixin, TestCase):

    def setUp(self):
        self.load_config()
        self.load_models()
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)

    def test_attributeA_access(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(siteconfig.TEST_A, "Test A default")

    def test_attributeB_access(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(siteconfig.TEST_B, 1)
        self.assertNotEqual(siteconfig.TEST_B, "1")

    def test_get_config_default_value_A(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(siteconfig.get_config("TEST_A")['value'],
                         self.config_dict['TEST_A']['default'])

    def test_get_config_has_proper_keys_A(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(self.config_dict["TEST_A"].keys() + ["value"],
                        siteconfig.get_config("TEST_A").keys(), )

    def test_get_config_has_proper_keys_B(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(self.config_dict["TEST_B"].keys() + ['value'],
                        siteconfig.get_config("TEST_B").keys(), )

    def test_get_config_default_value_B(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(siteconfig.get_config("TEST_B")['value'],
                         self.config_dict['TEST_B']['default'])

    '''
    def test_get_configs_default_value_A(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(siteconfig.get_configs(), siteconfig.get_default_configs())
    '''

    def test_set_config_A_update(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        siteconfig.set_config("TEST_A", "JOE")
        self.assertEqual(siteconfig.get_config("TEST_A")['value'], "JOE")
        self.assertEqual(siteconfig.TEST_A, "JOE")

    def test_set_config_B_update(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        siteconfig.set_config("TEST_B", 666)
        self.assertEqual(siteconfig.get_config("TEST_B")['value'], 666)
        self.assertEqual(siteconfig.TEST_B, 666)

    def test_invalid_attribute(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertFalse(hasattr(siteconfig, 'TEST_C'))


@override_settings(**settings)
class TestConfigActive(ModelsBaiscMixin, lib.SiteConfigMixin, TestCase):

    def _set_model_active_state(self, website, application, webapp):
        self.Website.objects.filter().update(active=website)
        self.Application.objects.filter().update(active=application)
        self.WebsiteApplication.objects.filter().update(active=webapp)

    def setUp(self):
        self.load_config()
        self.load_models()
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)

    def test_website_application_status__all_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(True, True, "enabled")
        self.assertEqual(siteconfig.website_application_status(), "enabled")

    def test_website_application_status__incorrect_status(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(True, True, "incorrect_status")
        self.assertEqual(siteconfig.website_application_status(), "disabled")

    def test_website_application_status__app_and_siteapp_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(False, True, "enabled")
        self.assertEqual(siteconfig.website_application_status(), "disabled")

    def test_website_application_status__wesite_and_siteapp_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(True, False, "enabled")
        self.assertEqual(siteconfig.website_application_status(), "disabled")

    def test_website_application_status__siteapp_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(False, False, "enabled")
        self.assertEqual(siteconfig.website_application_status(), "disabled")

    def test_website_application_status__nothing_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(False, False, "disabled")
        self.assertEqual(siteconfig.website_application_status(), "disabled")

    def test_get_curtain_message__nothing_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(False, False, "curtained")
        self.assertTrue("This site is undergoing scheduled maintenance" in siteconfig.get_curtain_message())

    def test_get_curtain_message__website_active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(True, False, "curtained")
        self.assertTrue("This site is undergoing scheduled maintenance" in siteconfig.get_curtain_message())

    def test_get_curtain_message__website_and_siteapp__active(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self._set_model_active_state(True, True, "curtained")
        self.assertTrue("This site is undergoing scheduled maintenance" in siteconfig.get_curtain_message())

    def test_dir(self):
        siteconfig = self.MyAppSiteConfig(website=self.site1_short_name)
        self.assertEqual(set(siteconfig.__dir__()), set(['TEST_A', 'TEST_B']))
