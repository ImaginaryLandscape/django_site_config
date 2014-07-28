from __future__ import unicode_literals
import logging
from site_config import utils, choices, settings
from .. import ConfigBackend

logger = logging.getLogger(__name__)

class SettingsBackend(ConfigBackend):

    def get(self, key, config_dict, application_short_name, website_short_name=None):
        """
        Get the key from the backend store and return the value.
        Return None if not found.
        
        RETURNS:
        This returns the appropriate meta dictionary back (for the 
        provided key), with the 'value' key added.  
        
        i.e
           {'default':"1234", "field":"django.forms.CharField", 
            "value":"5432", "help":"this is the help text."}
        
        """
        config_meta = config_dict[key]
        config_meta.update({'value':getattr(settings.settings, key, config_meta['default'])})
        return config_meta


    def mget(self, config_dict, application_short_name, website_short_name=None):
        """
        Get all the configuration values set for this application.
        
        RETURNS:
        This returns the config_dict with 'value' keys added to 
        each meta dictionary.
        
        i.e. 
          {
            "TEST_1":{
                'default':"1234", 
                "field":"django.forms.CharField", 
                "value":"5432", 
                "help":"this is the help text."},
            "TEST_2":{
                'default':"1234", 
                "field":"django.forms.CharField", 
                "value":"5432", 
                "help":"this is the help text."}
           }
        """
        raise NotImplementedError