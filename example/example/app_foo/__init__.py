from django import forms
import site_config

class FooConfig(site_config.SiteConfigBase):

    application_slug = "foo"
    application_verbose_name = "Foo App"

    def get_default_configs(self):
        return {'FOO_EMAIL':{'default':"joe@exampe.com",
                             'field':'django.forms.EmailField', 
                             'help':'Test A help text.'}, 
                "FOO_NUM":{'default':1, 
                           'field':'django.forms.IntegerField', 
                           'help':'Test B help text.'}}

site_config.settings.config_registry.register(FooConfig)
