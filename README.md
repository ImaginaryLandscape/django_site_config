from django import forms
import site_config

class MyAppSiteConfig(site_config.SiteConfigBase):

    application_slug = "myapp"
    application_verbose_name = "My Application"

    def get_default_configs(self):
        return {'TEST_A':{'default':"Test A default", 'field':forms.CharField, 'help':'Test A help text.'}, 
                "TEST_B":{'default':1, 'field':forms.IntegerField, 'help':'Test B help text.'}}

site_config.settings.config_registry.register(MyAppSiteConfig)



Add to INSTALLED_APPS

    'site_config',
    'site_config.backends.model_backend',