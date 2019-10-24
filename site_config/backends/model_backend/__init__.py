from __future__ import unicode_literals
import logging
from site_config import utils, choices
from .. import ConfigBackend

logger = logging.getLogger(__name__)


class DatabaseBackend(ConfigBackend):

    def get(self, key, config_dict, application_short_name, website_short_name=None):
        return self.mget(config_dict, application_short_name, website_short_name).get(key)

    def mget(self, config_dict, application_short_name, website_short_name=None):
        # Django 1.9+ registers apps;  this import is needed here to avoid
        # the AppRegistryNotReady exception
        from . import models
        # set a default 'value' in each nested config dict
        config_dict = utils.config_dict_value_from_default(config_dict)
        # lookup the site application
        site_app_list = models.WebsiteApplication.objects.filter(
                        website__short_name=website_short_name,
                        application__short_name=application_short_name,
        )
        # See this package's "models.py" for notes on the removal of "website_applications"
        # site_app_list = models.WebsiteApplication.objects.website_applications(
        #                website_short_name=website_short_name,
        #                application_short_name=application_short_name)
        if site_app_list.count() == 1:
            site_app = site_app_list[0]
            config_dict = site_app.get_config_options(config_dict)
        return config_dict

    def set(self, config_name, value, config_dict, application_short_name, website_short_name=None):
        config_dict = config_dict.copy()
        if config_name in config_dict:
            config_dict[config_name].update({'value': value})
        return self.mset(config_dict, application_short_name, website_short_name)

    def mset(self, config_dict, application_short_name, website_short_name=None):
        # Django 1.9+ registers apps;  this import is needed here to avoid
        # the AppRegistryNotReady exception
        from . import models
        try:
            site_app = models.WebsiteApplication.objects.get(
                                application__short_name=application_short_name,
                                website__short_name=website_short_name)
            site_app.set_config_options(config_dict)
        except models.WebsiteApplication.DoesNotExist:
            raise
        return site_app

    def website_application_status(self, application_short_name, website_short_name):
        # Django 1.9+ registers apps;  this import is needed here to avoid
        # the AppRegistryNotReady exception
        from . import models
        active = choices.WEBAPP_ACTIVE_STATE_DISABLED
        site_app_list = models.WebsiteApplication.objects.filter(
                        website__short_name=website_short_name,
                        application__short_name=application_short_name,
                        )
        if site_app_list.count() == 1:
            site_app = site_app_list[0]
            active = site_app.active_status()
        return active

    def get_curtain_message(self, application_short_name, website_short_name=None):
        # Django 1.9+ registers apps;  this import is needed here to avoid
        # the AppRegistryNotReady exception
        from . import models
        message = ("This site is undergoing scheduled maintenance."
                   "Thank you for your patience.")
        site_app_list = models.WebsiteApplication.objects.filter(
                        website__short_name=website_short_name,
                        application__short_name=application_short_name,
                        )
        if site_app_list.count() == 1:
            site_app = site_app_list[0]
            message_from_model = site_app.get_curtain_message()
            if message_from_model:
                message = message_from_model
        return message
