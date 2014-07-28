import mock
from copy import deepcopy
from django.test import TestCase
from django.test.utils import override_settings
from . import utils
   

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


settings = deepcopy(utils.settings_overrides)
settings.update(dict(SITECONFIG_BACKEND="site_config.backends.model_backend.DatabaseBackend"))

@override_settings(**settings)
class TestSiteConfigRegistry(utils.SiteConfigMixin, TestCase):
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
                         utils.settings_overrides['SITECONFIG_BACKEND'])


@override_settings(**settings)
class TestModelBackendBasicAccess(ModelsBaiscMixin, utils.SiteConfigMixin, TestCase):
    
    def setUp(self):
        self.load_config()
        self.load_models()
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        
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
class TestConfigActive(ModelsBaiscMixin, utils.SiteConfigMixin, TestCase):
    
    def _set_model_active_state(self, website, application, webapp):
        self.Website.objects.filter().update(active=website)
        self.Application.objects.filter().update(active=application)
        self.WebsiteApplication.objects.filter().update(active=webapp)

    def setUp(self):
        self.load_config()
        self.load_models()
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        
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
