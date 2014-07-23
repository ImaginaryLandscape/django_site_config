from . import settings
from . import utils

class SiteConfigBase(object):
    
    application_slug = "default_application"
    application_verbose_name = "Default Application"
    
    def get_default_config(self):
        """
        Returns a dictionary of configuration variables and their defaults. 
        The dictionary keys set the configuration variables.
        The dictionary values set the configuration default settings. 
         
        The configuration values should be upper-case by convention.
        """
        return {'TEST':"joe", "TESTB":1}
    
    def __init__(self, website=None):
        self.website = website
        super(SiteConfigBase, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())

    def __getattr__(self, name):
        if name in self.get_default_config().keys():
            return self.get_config(name)
        else:
            raise AttributeError("%r object has no attribute %r" %
                         (self.__class__, name))

    def get_config(self, key,):
        result = self._backend.get(key, self.get_default_config()[key], 
                                   self.application_slug, self.website, )
        return result
    
    def get_configs(self):
        return {k:getattr(self, k) for k in  self.get_default_config().keys() } 
    
    def set_config(self, key, value,):
        self._backend.set(key, value, self.application_slug, self.website)
        
    def __dir__(self):
        return self.get_default_config().keys()
    

settings.config_registry.register(SiteConfigBase)