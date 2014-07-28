
settings_overrides = dict(
    INSTALLED_APPS = (
        'django.contrib.admin', 
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions', 
        'django.contrib.messages',
        'django.contrib.staticfiles', 
        'site_config',
        'site_config.backends.model_backend',
    ),
    SITECONFIG_BACKEND = 'site_config.backends.model_backend.DatabaseBackend',
)


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
        
        self.site_config = __import__('site_config')
        class MyAppSiteConfig(self.site_config.SiteConfigBase):
            application_short_name = "myapp"
            application_verbose_name = "My Application"
        
            def get_default_configs(self):
                return config_dict
        self.MyAppSiteConfig = MyAppSiteConfig