

## CONFIGURATION ##
This application allows you to specify different siteconfig backends. 
The siteconfig backend is responsible for getting and setting settings
from/to a persistant location.  

Currently, two backends are present in this module:
  model_backend
  settings_backend
  
The model_backend stores configuration settings in a set of 
database models.  It allows for customizing the settings for a given
app inside of the admin interface and allows for different 
settings for different 'websites' inside an app.  Choosing this
backend enables an Django admin module for setting these settings.

The settings_backend is a simple backend that uses settings.py.
This is not dynamic; when an application needs a setting, this
backend just looks it up from settings.py. 


Add to INSTALLED_APPS in settings.py

    'site_config',

	# If using model_backend
    'site_config.backends.model_backend',
    
    # if using settings_backend
    'site_config.backends.settings_backend',


### GLOBAL SETTINGS in settings.py ###

SITECONFIG_BACKEND_DEFAULT (optional) = This specifies the default backend
that is to be used.  If this setting is not defined, it defaults
to the model_backend.

Valid values for this are as follows:
   "site_config.backends.model_backend.DatabaseBackend"  # model_backend
   "site_config.backends.settings_backend.SettingsBackend"  # settings_backend


### CONFIGURING THE settings_backend ###

Set the following in settings.py

- SITECONFIG_SITEAPP_STATUS (optional) - This sets whether or not apps using this module should
   be marked as active or not.  
   Valid values are: "disabled", "curtained", or "enabled"
   The default is "enabled"

- SITECONFIG_CURTAIN_MESSAGE (optional) = This sets the curtain message string when
   SITECONFIG_SITEAPP_STATUS is set to "curtained". 


### CONFIGURING THE  model_backend ###
  
You need to run the following if using the model_backend:

    ./manage.py syncdb
    ./manage.py migrate 


## USAGE ##

In order to use this system, you have to implement several things 
in your application. 

1.  Create a configuration class 
	
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
    
    See the example below:
    
    /path/to/myproject/myapp/__init__.py
	    
        import site_config
        
        class FooSiteConfig(site_config.SiteConfigBase):
        
            application_short_name = "foo"
            application_verbose_name = "Foo Application"
            
            # Optionally override if you want to customize the backend
            # used for a given config.
            def get_backend(self):
                backend = getattr(settings, 'SITECONFIG_BACKEND_DEFAULT',
                    'site_config.backends.model_backend.DatabaseBackend')
                return backend
            
            def get_default_configs(self):
                return {'TEST_A':{'default':"Test A default", 
                                  'field':forms.CharField, 
                                  'help':'Test A help text.'}, 
                        "TEST_B":{'default':1, 
                                  'field':forms.IntegerField, 
                                  'help':'Test B help text.'}}
        
        site_config.settings.config_registry.register(MyAppSiteConfig)

2.  Update and wrap your urls 
    
    In order to make use django_site_config's ability to enable and disable
    particular views, you need to wrap your urls as follows.  In order to 
    use this website switching functionality, you need to pass in the 
    "website" kwarg as part of the url string.
    
    /path/to/myproject/myapp/urls.py
    
        from django.conf.urls import patterns, include, url
        from site_config.decorators import enable_disable_website, decorated_includes
        from example.app_foo import FooConfig
        from .views import IndexView
        
        # Wrap a single url 
        
        urlpatterns = [
           url('^(?P<website>\w+)/foo/$', 
               enable_disable_website(IndexView.as_view(
                   template_name='index.html'), FooConfig), 
               {}, 
               name="app_foo_index"
           )
        ]
        
        # OR you can decorate an entire include
        
        urlpatterns += decorated_includes(lambda func: enable_disable_website(func, BarConfig),
            patterns('', url(r'^(?P<website>\w+)/bar/', include('example.app_bar.urls')))
        )
    
3.  Allow the optional 'website' kwarg into your views and use the 'website' 
      variable as desired. 

    /path/to/myproject/myapp/views.py

	    # Class based view example
		class IndexView(TemplateView):
		    
		    def get_context_data(self, **kwargs):
		        website = kwargs.get('website', None)
		        config = BarConfig(website=website)
		        kwargs['config'] = config
		        return kwargs
		
		# Function based view example
		def index(request, template_name, website=None, *args, **kwargs):
		    config = BarConfig(website=website)
		    return render_to_response(template_name,
		                              {'config':config,},
		                              context_instance=RequestContext(request))
	    


## EXAMPLE ##

    from osf.apps.core import FooSiteConfig
    c = FooSiteConfig(website="stjoseph")
    c.TEST_A
    c.TEST_B


## TEMPLATE OVERRIDES ##

You can override the template below to customize the curtain
page that displays when a Website Application as marked as
"curtained".  Note, the default template extends "base.html"
so this will need to be present in your application. 

   site_config/curtained.html

    
## TESTING ##

    pip install -e .[testing]
    cd example/
    ./manage.py test site_config



