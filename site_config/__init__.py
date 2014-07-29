from __future__ import unicode_literals
import logging
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.conf import settings
from . import utils, registry

logger = logging.getLogger(__name__)

class SiteConfigBase(object):
    
    application_short_name = "default_application"
    application_verbose_name = "Default Application"
    
    def get_backend(self):
        backend = getattr(settings, 'SITECONFIG_BACKEND',
            'site_config.backends.model_backend.DatabaseBackend')
        return backend
    
    def get_default_configs(self):
        """
        Returns a configuration dictionary of configuration variables and their defaults. 
        The dictionary keys set the configuration variables.
        The dictionary values are another nested dictionary.
          This nested dictionary must contain 3 keys:
            default = the default value that the key will take
            field = a django Field instance used to validate the value
            help (optional) = a help text entry that describes the key 
         
        The configuration values should be upper-case by convention.
        """
        return {'EXAMPLE_A':{'default':"Test A default",
                             'field':'django.forms.CharField',
                             'help':'Test A help text.'},
                "EXAMPLE_B":{'default':1,
                             'field':'django.forms.IntegerField',
                             'help':'Test B help text.'}}
    
    def __init__(self, website=None):
        self.website = website
        for k, v in self.get_default_configs().items():
            if 'default' not in v:
                raise ImproperlyConfigured("Config value dict %s must have a 'default' key." % (v))
            elif 'field' not in v:
                raise ImproperlyConfigured(
                    "Config value dict %s must have a 'field' key, which is a valid django field." % (v))
        super(SiteConfigBase, self).__setattr__('_backend',
            utils.import_module_attr(self.get_backend())())

    def __getattr__(self, name):
        if name in self.get_default_configs().keys():
            return self.get_config(name)['value']
        else:
            raise AttributeError("%r object has no attribute %r" %
                         (self.__class__, name))

    def get_config(self, key,):
        """
        This method gets the configuration dictionary from get_default_configs() 
        and looks up the provided key from that dictionary, which returns the nested 
        configuration dictionary for that key.
        
        That nested dictionary is then passed to the storage backend to be 
        updated with a new 'value' key.  That value key is either the result 
        of the backend lookup, or the value of the 'default' key. 
        
        Example Return Value:
                {'default':"Test A default", 'field':forms.CharField, 
                           'help':'Test A help text.', 'value':"looked-up value A"}
        """
        result = self._backend.get(key, self.get_default_configs(), 
                                   self.application_short_name, self.website, )
        return result
    
    def get_configs(self):
        """
        This method gets the configuration dictionary from get_default_configs() 
        and passes it to the storage backend. 
        
        The storage backend returns a similar dictionary with the value key added to the
        nested dictionaries.  These value keys are the result of the configuration lookup
        or the default specified by the default nested dictionary keys.
        Example Return Value:
                {"EXAMPLE_A":{'default':"Test A default", 
                              'field':forms.CharField,
                              'help':'Test A help text.',
                              'value':"looked-up value A"}, 
                 "EXAMPLE_B":{'default':1, 
                              'field':forms.IntegerField, 
                              'help':'Test B help text.', 
                              'value':"looked-up value B"}}
        """
        return self._backend.mget(self.get_default_configs(), self.application_short_name, self.website)
    
    def set_config(self, key, value,):
        self._backend.set(key, value, self.get_default_configs(), self.application_short_name, self.website)
    
    def website_application_status(self):
        return self._backend.website_application_status(self.application_short_name, self.website)
    
    def get_curtain_message(self):
        return self._backend.get_curtain_message(self.application_short_name, self.website)
    
    def __dir__(self):
        return self.get_default_configs().keys()
    

#registry.config_registry.register(SiteConfigBase)