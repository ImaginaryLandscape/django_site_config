## ABOUT ##

This module provides you an API that lets you code django
applications such that those apps can segment themselves 
into multiple sections and have different settings for each
section.  

For example, say I want to use the same app under two different
url paths and have different behavior (different settings) for both. 

    /mysite1/myapp/
    /mysite2/myapp/

Also, say I want to enable or disable individual apps on those different 
urls, via an admin interface. 

Also, say I want to have a consistent way to define settings for those apps.


This module helps you to accomplish those things. 

## INSTALL ##

Install from pip

    pip install site_config

Install from Github

    git clone https://github.com/ImaginaryLandscape/django_site_config.git


## CONFIGURATION ##
This application allows you to specify different siteconfig backends. 
The siteconfig backend is responsible for getting and setting settings
from/to a persistent location.  

Currently, two backends are present in this module:

 -   model_backend
 -   settings_backend
  
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
                                  'field':'django.forms.CharField', 
                                  'help':'Test A help text.'}, 
                        "TEST_B":{'default':1, 
                                  'field':'django.forms.IntegerField', 
                                  'help':'Test B help text.'}}
        
        site_config.registy.config_registry.register(MyAppSiteConfig)

2.  Enable and disable urls via enable_disable_website() decorator
    
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
           url('^(?P<website>[\w-]+)/foo/$', 
               enable_disable_website(IndexView.as_view(
                   template_name='index.html'), FooConfig), 
               {}, 
               name="app_foo_index"
           )
        ]
        
        # OR you can decorate an entire include
        
        urlpatterns += decorated_includes(lambda func: enable_disable_website(func, BarConfig),
            patterns('', url(r'^(?P<website>[\w-]+)/bar/', include('example.app_bar.urls')))
        )
   
   Note: You can also use this enable_disable_website() function to decorate
   a django CBV or FBV according to the django documentation.  
   
   Note: Your views must accept the 'website' keyword argument. 
          
3. Allow template overrides 

    This module also provides a means to override templates for a specific site. 
    
    FOR FUNCTION BASED VIEWS 
    
    Normally, if a FBV defines a template_name parameter in the url, say
    "index.html", the view will lookup that template file via the normal
    template loader chain.
    
    However, the website_template_override() decorator will first try 
    to lookup a url at "[website]/index.html" and then fall back to using
    the "index.html".  

    /path/to/myproject/myapp/urls.py
    
        # Wrap a single url 
        
        urlpatterns = [
            url('^(?P<website>[\w-]+)/foo/$', 
                website_template_override(IndexView.as_view(
                template_name='index.html')), 
                {}, 
                name="app_foo_index"
            )
        ]
        
        # OR you can decorate an entire include
        
        urlpatterns += decorated_includes(website_template_override,
            patterns('', url(r'^(?P<website>[\w-]+)/bar/', 
                             include('example.app_bar.urls')))
        )
        
        # OR you can use both decorators at once on an entire include.
        urlpatterns += decorated_includes(
            (
                lambda func: enable_disable_website(func, BarConfig),
                website_template_override,
            ),
            patterns('', url(r'^(?P<website>[\w-]+)/bar/', 
                             include('example.app_bar.urls')))
        )
     
    You then need to accept the website variable as a keyword argument
    to your view function.  The website variable can be used in your view logic.
    
    /path/to/myproject/myapp/views.py
        
        # Function based view example
        def index(request, template_name, website=None, *args, **kwargs):
            config = BarConfig(website=website)
            return render_to_response(template_name,
                {'config':config,},
                context_instance=RequestContext(request))

    FOR CLASS BASED VIEWS
    
    You should use the WebsiteOverrideTemplateViewMixin to allow for the 
    template override behavior.  
    
    /path/to/myproject/myapp/views.py
        
		from site_config.utils import WebsiteOverrideTemplateViewMixin
		from site_config.decorators import website_template_override
		from example.app_bar import BarConfig
		
		class IndexView(WebsiteOverrideTemplateViewMixin, TemplateView):
		    
		    def dispatch(self, request, *args, **kwargs):
		        self.website = kwargs.get('website', None)
		        self.config = BarConfig(website=self.website)
		        return super(IndexView, self).dispatch(request, *args, **kwargs)
		    
		    def get_context_data(self, **kwargs):
		        kwargs['config'] = self.config
		        kwargs['website'] = self.website
		        return kwargs
        
4.  You can access settings in the view or template by calling the settings
    like you would an attribute on the config class.  
    
    Here is a usage example:

	    from example.app_foo import FooConfig
	    c = FooConfig(website="joesite")
	    c.TEST_A
	    c.TEST_B
	    
    Note:
    in order for the settings to be looked up dynamically (on each request), the
    config class must be instantiated inside the view with the proper
    website passed to the constructor (or None) on every request to the view.


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



