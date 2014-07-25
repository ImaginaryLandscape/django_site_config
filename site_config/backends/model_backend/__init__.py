from __future__ import unicode_literals
import logging
from site_config import utils
from .. import ConfigBackend
from . import models

logger = logging.getLogger(__name__)

class DatabaseBackend(ConfigBackend):

    def get(self, key, config_dict, application_slug, website=None):
        return self.mget(config_dict, application_slug, website).get(key)
    
    def mget(self, config_dict, application_slug, website=None):
        # set a default 'value' in each nested config dict
        config_dict = utils.config_dict_value_from_default(config_dict)
        # lookup the site application
        site_app_list = models.WebSiteApplication.objects.website_applications(
                        website_slug=website, application_slug=application_slug, 
                        )
        #raise Exception(site_app_list.values_list('website__slug', 'application__slug', ))
        if site_app_list.count() == 1:
            site_app = site_app_list[0]
            config_dict = site_app.get_config_options(config_dict)
        return config_dict
    
    def set(self, config_name, value, config_dict, application_slug, website=None):
        config_dict = config_dict.copy()
        if config_name in config_dict:
            config_dict[config_name].update({'value':value})
        return self.mset(config_dict, application_slug, website)
    
    def mset(self, config_dict, application_slug, website=None):
        try:
            site_app = models.WebSiteApplication.objects.get(
                                application__slug=application_slug, website__slug=website)
            site_app.set_config_options(config_dict)
        except models.WebSiteApplication.DoesNotExist:
            raise 
        return site_app