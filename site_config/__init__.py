from django.core.exceptions import ImproperlyConfigured
from django import forms
from . import settings
from . import utils


class SiteConfigBase(object):
    
    application_slug = "default_application"
    application_verbose_name = "Default Application"
    
    def get_default_configs(self):
        """
        Returns a dictionary of configuration variables and their defaults. 
        The dictionary keys set the configuration variables.
        The dictionary values are another nested dictionary.
          This nested dictionary must contain 3 keys:
            default = the default value that the key will take
            field = a django Field instance used to validate the value
            help (optional) = a help text entry that describes the key 
         
        The configuration values should be upper-case by convention.
        """
        return {'EXAMPLE_A':{'default':"Test A default", 'field':forms.CharField, 'help':'Test A help text.'}, 
                "EXAMPLE_B":{'default':1, 'field':forms.IntegerField, 'help':'Test B help text.'}}
    
    def __init__(self, website=None):
        self.website = website
        for k, v in self.get_default_configs().items():
            if 'default' not in v:
                raise ImproperlyConfigured("Config value dict %s must have a 'default' key." % (v))
            elif 'field' not in v:
                raise ImproperlyConfigured(
                    "Config value dict %s must have a 'field' key, which is a valid django field." % (v))
        super(SiteConfigBase, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())

    def __getattr__(self, name):
        if name in self.get_default_configs().keys():
            return self.get_config(name)['value']
        else:
            raise AttributeError("%r object has no attribute %r" %
                         (self.__class__, name))

    def get_config(self, key,):
        result = self._backend.get(key, self.get_default_configs()[key], 
                                   self.application_slug, self.website, )
        return result
    
    def get_configs(self):
        return {k:self.get_config(k) for k in  self.get_default_configs().keys() } 
    
    def set_config(self, key, value,):
        self._backend.set(key, value, self.application_slug, self.website)
        
    def __dir__(self):
        return self.get_default_configs().keys()
    

settings.config_registry.register(SiteConfigBase)