from __future__ import unicode_literals
import logging
from site_config import utils, choices
from .. import ConfigBackend
from . import models

logger = logging.getLogger(__name__)

class DatabaseBackend(ConfigBackend):

    def get(self, key, config_dict, application_slug, website_slug=None):
        return self.mget(config_dict, application_slug, website_slug).get(key)
    
    def mget(self, config_dict, application_slug, website_slug=None):
        # set a default 'value' in each nested config dict
        config_dict = utils.config_dict_value_from_default(config_dict)
        # lookup the site application
        site_app_list = models.WebsiteApplication.objects.website_applications(
                        website_slug=website_slug, application_slug=application_slug, 
                        )
        if site_app_list.count() == 1:
            site_app = site_app_list[0]
            config_dict = site_app.get_config_options(config_dict)
        return config_dict
    
    def set(self, config_name, value, config_dict, application_slug, website_slug=None):
        config_dict = config_dict.copy()
        if config_name in config_dict:
            config_dict[config_name].update({'value':value})
        return self.mset(config_dict, application_slug, website_slug)
    
    def mset(self, config_dict, application_slug, website_slug=None):
        try:
            site_app = models.WebsiteApplication.objects.get(
                                application__slug=application_slug, website__slug=website_slug)
            site_app.set_config_options(config_dict)
        except models.WebsiteApplication.DoesNotExist:
            raise 
        return site_app
    
    def is_website_application_active(self, application_slug, website_slug):
        active = choices.WEBAPP_ACTIVE_STATE_DISABLED
        site_app_list = models.WebsiteApplication.objects.website_applications(
                        website_slug=website_slug, application_slug=application_slug, 
                        )
        if site_app_list.count() == 1:
            site_app = site_app_list[0]
            active = site_app.is_active()
        return active