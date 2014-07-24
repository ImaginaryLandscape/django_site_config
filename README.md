import site_config

class MyAppSiteConfig(site_config.SiteConfigBase):

    application_slug = "myapp"
    application_verbose_name = "My Application"

    def get_default_config(self):
        return {"TESTB":"JOE JAZ", "TESTC":"RETURN TESTC"}


site_config.settings.config_registry.register(MyAppSiteConfig)



Add to INSTALLED_APPS

    'site_config',
    'site_config.backends.model_backend',