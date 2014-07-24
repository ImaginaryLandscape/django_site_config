from django import forms
import site_config

class MyAppSiteConfig(site_config.SiteConfigBase):

    application_slug = "app1"
    application_verbose_name = "My Application 1"

    def get_default_config(self):
        return {'APP1_EMAIL':{'default':"Test A default", 'field':forms.EmailField, 'help':'Test A help text.'}, 
                "APP1_NUM":{'default':1, 'field':forms.IntegerField, 'help':'Test B help text.'}}

site_config.settings.config_registry.register(MyAppSiteConfig)

