
# INSTALL:

Add to INSTALLED_APPS

    'site_config',
    'site_config.backends.model_backend',


# USAGE

Create add the following class in a django app's __init__.py, models.py
or some other location that is called when django first executes.
Define "application_short_name" and "application_verbose_name" attributes.

Implement the "get_default_configs()" method.  This must return a 
configuration dictionary where the keys are the configuration 
variables for the application, and the values are nested metadata 
dictionaries.

Each nested dictionary must contain 3 keys:
 - default = the default value that the key will take
 - field = a django Field instance used to validate the value
 - help (optional) = a help text entry that describes the key 
 - choices (optional) = a list of tuples constraining the input.
   Only works with fields that are like ChoiceField that take
   choices as part of the constructor
    i.e. (('a_short_name','A text'),('b_short_name', 'B text'))

You also need to register the config class with the "register()" method.

See the example below 

	import site_config
	
	class MyAppSiteConfig(site_config.SiteConfigBase):
	
	    application_short_name = "myapp"
	    application_verbose_name = "My Application"
	
	    def get_default_configs(self):
	        return {'TEST_A':{'default':"Test A default", 'field':forms.CharField, 'help':'Test A help text.'}, 
	                "TEST_B":{'default':1, 'field':forms.IntegerField, 'help':'Test B help text.'}}
	
	site_config.settings.config_registry.register(MyAppSiteConfig)



# EXAMPLE:

    from osf.apps.core import FormbundleConfig
    c = FormbundleConfig(website="stjoseph")
    c.TEST_A
    c.TEST_B


# TEMPLATE OVERRIDES

You can override the template below to customize the curtain
page that displays when a Website Application as marked as
"curtained".  Note, the default template extends "base.html"
so this will need to be present in your application. 

   site_config/curtained.html

    
# TESTING

  pip install -e .[testing]
  cd example/
  ./manage.py test site_config



# SETTINGS

## Global settings
SITECONFIG_BACKEND = 
 Current options are as follows:
 - site_config.backends.model_backend.DatabaseBackend  
 - site_config.backends.settings_backend.SettingsBackend

## settings_backend settings
SITECONFIG_ACTIVE = 
SITECONFIG_CURTAIN_MESSAGE = 

