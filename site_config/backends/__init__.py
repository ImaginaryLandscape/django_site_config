from __future__ import unicode_literals


class ConfigBackend(object):

    def get(self, key, config_dict, application_slug, website_slug=None):
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
        raise NotImplementedError

    def mget(self, config_dict, application_slug, website_slug=None):
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

    def set(self, config_name, value, config_dict, application_slug, website_slug=None):
        """
        Add the value to the backend store given the key.
        """
        raise NotImplementedError

    def mset(self, config_dict, application_slug, website_slug=None):
        """
        This saves all of the config values to the backend.
        """
        raise NotImplementedError