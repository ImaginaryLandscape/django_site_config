from .. import ConfigBackend
from . import models

class DatabaseBackend(ConfigBackend):

    def get(self, key, default, application_slug, website=None):
        return_value = default
        site_app = models.WebSiteApplication.objects.active_website_applications(
                        website_slug=website, application_slug=application_slug, 
                        )
        if site_app.count() == 1:
            return_value = site_app[0].get_config_option(key)
        return return_value
    
    def set(self, key, value, application_slug, website=None):
        created = None
        try:
            obj = models.ConfigurationKeyValue.objects.get(key=key, 
                                application_slug=application_slug, website=website)
            obj.value = value
            obj.save()
            created = False
        except models.ConfigurationKeyValue.DoesNotExist:
            obj = models.ConfigurationKeyValue(key=key, value=value,
                                application_slug=application_slug, website=website)
            obj.save()
            created = True
        return created