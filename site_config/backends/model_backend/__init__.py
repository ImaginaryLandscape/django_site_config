from .. import ConfigBackend
from . import models

class DatabaseBackend(ConfigBackend):

    def get(self, key, lookup_dict, application_slug, website=None):
        site_app = models.WebSiteApplication.objects.active_website_applications(
                        website_slug=website, application_slug=application_slug, 
                        )
        if site_app.count() == 1:
            lookup_dict.update({'value':site_app[0].get_config_option(key, lookup_dict['default'])})
        else:
            lookup_dict.update({'value':lookup_dict['default']})
        return lookup_dict
    
    def set(self, key, value, application_slug, website=None):
        created = None
        try:
            obj = models.WebSiteApplication.objects.get(
                                application__slug=application_slug, website=website)
            obj.value = value
            obj.save()
            created = False
        except models.WebSiteApplication.DoesNotExist:
            obj = models.ConfigurationKeyValue(
                                application__slug=application_slug, website=website)
            obj.save()
            created = True
        return created