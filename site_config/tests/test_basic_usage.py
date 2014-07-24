import mock
from django.test import TestCase
from django.test.utils import override_settings
from . import utils

class SiteConfigMixin(object):

    def load_config(self):
        self.site_config = __import__('site_config')
        class MyAppSiteConfig(self.site_config.SiteConfigBase):
            application_slug = "myapp"
            application_verbose_name = "My Application"
        
            def get_default_configs(self):
                return {'TEST_A':{'default':
                                  "Test A default", 
                                  'field':'django.forms.CharField', 
                                  'help':'Test A help text.'}, 
                        "TEST_B":{'default':1, 
                                  'field':'django.forms.IntegerField', 
                                  'help':'Test B help text.'}}
        self.MyAppSiteConfig = MyAppSiteConfig
   

class ModelsBaiscMixin(object):
    def load_models(self):
        self.sites = []
        site = self.site_config.backends.model_backend.models.WebSite(name="JOE SITE", slug='joe')
        site.save()
        self.sites.append(site)

        site = self.site_config.backends.model_backend.models.WebSite(
                                    name="John Site", slug='john', active=True)
        site.save()
        self.sites.append(site)
        
        
        self.apps = []
        app = self.site_config.backends.model_backend.models.Application(
                                    name="Formfun", slug='formfun', active=True)
        app.save()
        self.apps.append(app)

        self.apps = []
        app = self.site_config.backends.model_backend.models.Application(
                                    name="DJhelper", slug='djhelper', active=True)
        app.save()
        self.apps.append(app)

        webapp = self.site_config.backends.model_backend.models.WebSiteApplication(
                                    website=self.sites[0], application=self.apps[0],
                                    active=True)
        webapp.save()
        self.webapps = []
        self.webapps.append(webapp)

@override_settings(**utils.settings_overrides)
class TestConfigRegistry(SiteConfigMixin, TestCase):
    def setUp(self):
        self.load_config()

    def test_register_site_config(self):
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        self.assertIsNotNone(self.site_config.settings.config_registry.get_config_class('myapp'), )

    def test_register_site_config_verbose_name(self):
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        self.assertEqual(self.site_config.settings.config_registry.get_config_class('myapp')[0], 
                         self.MyAppSiteConfig.application_verbose_name) 

    def test_register_site_config_slug(self):
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        config_class = self.site_config.settings.config_registry.get_config_class('myapp')[1]
        self.assertEqual(config_class.application_slug, 
                         self.MyAppSiteConfig.application_slug) 
    

@override_settings(**utils.settings_overrides)
class TestConfigBasic(ModelsBaiscMixin, SiteConfigMixin, TestCase):
    def setUp(self):
        self.load_config()
        self.load_models()
        self.site_config.settings.config_registry.register(self.MyAppSiteConfig)
        
    def test_attributeA_access(self):
        siteconfig = self.MyAppSiteConfig(self.MyAppSiteConfig.application_slug)
        self.assertEqual(siteconfig.TEST_A, "Test A default")

    def test_attributeB_access(self):
        siteconfig = self.MyAppSiteConfig(self.MyAppSiteConfig.application_slug)        
        self.assertEqual(siteconfig.TEST_B, 1)
        self.assertNotEqual(siteconfig.TEST_B, "1")

