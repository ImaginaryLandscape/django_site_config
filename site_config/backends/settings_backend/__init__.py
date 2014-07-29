from __future__ import unicode_literals
import logging
from site_config import utils, choices, registry
from django.conf import settings
from .. import ConfigBackend

logger = logging.getLogger(__name__)

class SettingsBackend(ConfigBackend):

    def get(self, key, config_dict, application_short_name, website_short_name=None):
        config_meta = config_dict[key]
        config_meta.update({'value':getattr(settings, key, config_meta['default'])})
        return config_meta

    def website_application_status(self, application_short_name, website_short_name=None):
        return getattr(settings, 'SITECONFIG_ACTIVE', choices.WEBAPP_ACTIVE_STATE_ENABLED)        

    def get_curtain_message(self, application_short_name, website_short_name=None):
        return getattr(settings, 'SITECONFIG_CURTAIN_MESSAGE', 
                       "This site is undergoing scheduled maintenance." 
                       "Thank you for your patience.")