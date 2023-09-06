## ABOUT ##

This package allows an app to run with different configuration settings under
different paths (URLs).

For example, the two url paths below both make use of the app "myapp", but
"site_config" can help you to configure unique behavior for each.

    /mysite1/myapp/
    /mysite2/myapp/

Each path can be enabled or disabled individually in the Django admin.


## INSTALLATION ##

Install from pip

    pip install site-config

Install from Github

    git clone https://github.com/ImaginaryLandscape/django_site_config.git


## CONFIGURATION ##

This application can retrieve the configurations for the various paths using one
of two "backends":

 - the model backend, which uses a set of Django models
 
 - the settings backend, which uses the "settings" module
  
The model backend allows for customizing the settings for a given app via the
Django admin interface.

The settings backend is simpler, but not dynamic. Changes must be defined in the
"settings.py" module.


To enable Siteconfig, adjust the "INSTALLED_APPS" setting in "settings.py".

  - Add 'site_config'
  - If using the model backend, add 'site_config.backends.model_backend'
  - If using the settings backend, add 'site_config.backends.settings_backend'


Site-specific configurations can be made available to your templates by adding
the following context processor to the 'OPTIONS' section of the 'TEMPLATES'
setting in "settings.py":

  'site_config.context_processors.add_site_specific_options'


Site-specific base templates can also be configured by adding the following
context processor to the 'OPTIONS' section of the 'TEMPLATES' setting in
"settings.py":

    'site_config.context_processors.decide_base_template'

This sets a new context variable `base_template` so that the contents of your
"base.html" template can extend a variable.  Instead of including all template
logic in your project's "base.html" template, you can move this logic to another
template ("base_site.html", for instance) and let "base.html" be:

    {% extends base_template|default:"base_site.html" %}

Now the template "base_site.html" will be used if it is present in your site's
"templates" directory.


### GLOBAL SETTINGS in settings.py ###

SITECONFIG_BACKEND_DEFAULT (optional) = This specifies the default backend that
is to be used.  If this setting is not defined, it defaults to the model
backend.

Valid values for this are as follows:

    "site_config.backends.model_backend.DatabaseBackend"  # model_backend
    "site_config.backends.settings_backend.SettingsBackend"  # settings_backend


SITECONFIG_BASE_TEMPLATE (optional) = This specifies what the default base
template should be when using the `decide_base_template` context processor.  If
this context processor is not used, this setting has no effect.


### CONFIGURING THE model_backend ###
  
You need to run the following if using the model_backend:

    ./manage.py makemigrations
    ./manage.py migrate 


If the model backend is used, the Website, Application, and WebsiteApplication
models defined in models.py should appear in the Django admin. If the settings
backend is used, they should not appear.


### CONFIGURING THE settings_backend ###

Set the following in settings.py

- SITECONFIG_SITEAPP_STATUS (optional) - This sets whether or not apps using
   this module should be marked as active or not.  Valid values are: "disabled",
   "curtained", or "enabled" The default is "enabled"

- SITECONFIG_CURTAIN_MESSAGE (optional) = This sets the curtain message string
   when SITECONFIG_SITEAPP_STATUS is set to "curtained".


## USAGE ##

In order to use this system, you must do the following:

1.  Create a configuration class 
  
    Add a subclass of "site_config.SiteConfigBase" to your app's
    "__init__.py". The class should define "application_short_name" and
    "application_verbose_name" attributes.
    
    The class should also implement the "get_default_configs()" method.  This
    must return a configuration dictionary where the keys are the configuration
    variables for the application, and the values are nested metadata
    dictionaries.
    
    Each nested dictionary must contain two keys:

      - default = the default value that the key will take

      - field = a django Field instance used to validate the value

    The dictionary may also contain an optional "help" key

      - help (optional) = help text to accompany the field in the Django admin


    If the field is a type that takes a "choices" parameter in its constructor,
    the following two keys can be used to constrain the input to a defined set
    of choices:

      - choices (optional) = a list of tuples

      - queryset (optional) = a Django queryset 
     

    Finally, you must register the config class with the "register()" method.
    
    EXAMPLE:
    
    /path/to/myproject/myapp/__init__.py
      
        import site_config
        
        class FooSiteConfig(site_config.SiteConfigBase):
        
            application_short_name = "foo"
            application_verbose_name = "Foo Application"
        
            def get_default_configs(self):
                return {"TEST_A": {"default": "Test A default", 
                                   "field": "django.forms.CharField", 
                                   "help": "Test A help text."}, 
                        "TEST_B": {"default": 1, 
                                   "field":" django.forms.ChoiceField",
                                   "choices": [(1, 'one'), (2, 'two')], 
                                   "help": "Test B help text."}}
        
        site_config.registy.config_registry.register(FooSiteConfig)


2.  Enable and disable urls via enable_disable_website() decorator
    
    To make use of Siteconfig's ability to enable and disable particular
    views, you must wrap your urls as follows.  You must also pass in the
    "website" kwarg as part of the url string.
    
    /path/to/myproject/myapp/urls.py

        from django.conf.urls import include
        from django.urls import re_path
        from site_config.decorators import enable_disable_website, decorated_includes
        from example.app_foo import FooConfig
        from .views import IndexView

        urlpatterns = [
            # Other url patterns assigned here
        ]

        # Wrap a single url 
        urlpatterns += [
           re_path(r'^(?P<website>[\w-]+)/foo/$', 
               enable_disable_website(
                   IndexView.as_view(),
                   FooConfig
               ), kwargs={}, name="app_foo_index"
           )
        ]
        
        # OR you can decorate an entire include
        urlpatterns += decorated_includes(
            lambda func: enable_disable_website(func, BarConfig),
            [re_path(r'^(?P<website>[\w-]+)/bar/', include('example.app_bar.urls'))]
        )
   
          
3. Allow template overrides 

    Siteconfig also provides a means to override templates for a specific site.
    
    FOR FUNCTION-BASED VIEWS 
    
    Normally, if a path in "urls.py" receives a value for "template_name" (e.g.,
    "index.html"), the view will look up that template file via the normal
    template loader chain.

    However, the website_template_override() decorator will first look for a
    template at "[website]/index.html" before falling back to using the more
    general "index.html".

    /path/to/myproject/myapp/urls.py

        from django.conf.urls import include
        from django.urls import re_path
        from site_config.decorators import enable_disable_website, decorated_includes, website_template_override
        from example.app_foo import FooConfig

        urlpatterns = [
            # Other url patterns assigned here
        ]

        # Wrap a single url    
        urlpatterns += [
            re_path(r'^(?P<website>[\w-]+)/foo/$', 
                website_template_override(
                    IndexView.as_view(template_name='index.html')
                ), kwargs={}, name="app_foo_index"
            )
        ]
        
        # OR you can decorate an entire include
        urlpatterns += decorated_includes(website_template_override,
            [re_path(r'^(?P<website>[\w-]+)/bar/', include('example.app_bar.urls'))]
        )

        # OR you can use both decorators at once on an entire include.
        urlpatterns += decorated_includes(
            lambda func: enable_disable_website(func, BarConfig),
            website_template_override,
            [re_path(r'^(?P<website>[\w-]+)/bar/', include('example.app_bar.urls'))]
        )
     
    You then need to accept the website variable as a keyword argument to your
    view function.  The website variable can be used in your view logic.
    
    /path/to/myproject/myapp/views.py
        
        # Function based view example
        def index(request, template_name, website=None, *args, **kwargs):
            config = BarConfig(website=website)
            return render(request, template_name, {'config':config})


    FOR CLASS-BASED VIEWS
    
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
                return super().dispatch(request, *args, **kwargs)
        
            def get_context_data(self, **kwargs):
                kwargs['config'] = self.config
                kwargs['website'] = self.website
                return kwargs
        

4.  You can access settings in the view or template by calling the settings like
    you would an attribute on the config class.
    
    Here is a usage example:

        from example.app_foo import FooConfig
        c = FooConfig(website="joesite")
        c.TEST_A
        c.TEST_B
      
    Note: in order for the settings to be looked up dynamically (on each
    request), the config class must be instantiated inside the view with the
    proper website passed to the constructor (or None) on every request to the
    view.


5.  However, note that a WebsiteApplication's configuration values (e.g., "TEST_A" from the example
above) will be automatically available in the template if you add the "add_site_specific_options"
context processor to your project's "TEMPLATES" setting like this:

        TEMPLATES = [
            {
                # other keys in the "TEMPLATES" dictionary ("BACKEND", etc.)
                'OPTIONS': {
                    'context_processors': [
                        # other context processors
                        'site_config.context_processors.add_site_specific_options',
                    ],
                },
            },
        ]


    The variable can then be accessed in the template via the "siteconfig_options" dictionary:

        {{ siteconfig_options.TEST_A }}

    The value will already be the appropriate one for the relevant website and app.
    

## TEMPLATE OVERRIDES ##

You can override the template below to customize the curtain page that displays
when a WebsiteApplication as marked as "curtained".  Note, the default template
extends "base.html" so this will need to be present in your application.

   site_config/curtained.html
