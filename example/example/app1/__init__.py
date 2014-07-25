from django import forms
import site_config

class MyAppSiteConfig(site_config.SiteConfigBase):

    application_slug = "app1"
    application_verbose_name = "My Application 1"

    def get_default_configs(self):
        return {'APP1_EMAIL':{'default':"joe@exampe.com", 'field':'django.forms.EmailField', 'help':'Test A help text.'}, 
                "APP1_NUM":{'default':1, 'field':'django.forms.IntegerField', 'help':'Test B help text.'}}

site_config.settings.config_registry.register(MyAppSiteConfig)


class MyFunConfig(site_config.SiteConfigBase):

    application_slug = "myfun"
    application_verbose_name = "My Fun App 1"

    def get_default_configs(self):
        return {'MYFUN_EMAIL':{'default':"joe@exampe.com", 
                               'field':'django.forms.CharField', 
                               'help':'Test A help text.'}, 
                "MYFUN_NUM":{'default':1, 
                             'field':'django.forms.IntegerField', 
                             'help':'Enter a number.'},
                "MYFUN_CHAR":{'default':"b", 
                              'field':'django.forms.ChoiceField', 
                              'help':'Test B help text.', 
                              'choices':(('a',"A choice"),("b","B Choice"),)},
                }

site_config.settings.config_registry.register(MyFunConfig)

