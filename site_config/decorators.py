from __future__ import unicode_literals
import logging
import inspect

from django.http import Http404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from . import choices, utils

logger = logging.getLogger(__name__)

###### Decorator Utilities


def decorated_includes(wrapping_functions, patterns_rslt):
    '''
    SOURCE: http://stackoverflow.com/questions/2307926/is-it-possible-to-decorate-include-in-django-urls-with-login-required
    
    Used to require 1..n decorators in any view returned by a url tree

    Usage:
      urlpatterns = decorated_includes(func,patterns(...))
      urlpatterns = decorated_includes((func,func,func),patterns(...))

    Note:
      Use functools.partial to pass keyword params to the required 
      decorators. If you need to pass args you will have to write a 
      wrapper function.

    Example:
      from functools import partial

      urlpatterns = decorated_includes(
          partial(login_required,login_url='/accounts/login/'),
          patterns(...)
      )
    '''
    if not hasattr(wrapping_functions,'__iter__'): 
        wrapping_functions = (wrapping_functions,)

    return [
        _wrap_instance__resolve(wrapping_functions, instance)
        for instance in patterns_rslt
    ]

def _wrap_instance__resolve(wrapping_functions, instance):
    if not hasattr(instance,'resolve'): return instance
    resolve = getattr(instance,'resolve')

    def _wrap_func_in_returned_resolver_match(*args,**kwargs):
        rslt = resolve(*args,**kwargs)
        

        if not hasattr(rslt,'func'):return rslt
        f = getattr(rslt,'func')

        for _f in reversed(wrapping_functions):
            # @decorate the function from inner to outter
            f = _f(f)

        setattr(rslt,'func',f)

        return rslt

    setattr(instance,'resolve',_wrap_func_in_returned_resolver_match)

    return instance



###### Decorator Functions

def enable_disable_website(the_func, config_class):
    """
    This determines whether or not the view should be
    considered active, curtained, or disabled (404)
    for the webapp based on the value of    
    website_application_status() from the backend.
    
    This takes a view function and a config class.
    The view function should contain a 'website' 
    keyword argument, either as part of the url regex 
    or passed in via the url()'s kwargs dictionary.
    
    If the webapp is active, the view is processed as normal.
    If the webapp is curtained, a 404 is returned and a
    curtain message is printed to the screen (as defined
    by the get_curtain_message() backend method.)
    If the webapp is disabled, a 404 is returned. 
    
    """

    def _decorated(*args, **kwargs):
        website = kwargs.get('website', None)
        app_config = config_class(website=website)
        active_state = app_config.website_application_status()
        if active_state == choices.WEBAPP_ACTIVE_STATE_CURTAINED:
            if args[0].user.is_authenticated() and args[0].user.is_superuser:
                pass
            else:
                logger.debug("Website Application curtained %s - %s" % (website, app_config.application_short_name))
                return HttpResponseNotFound(render_to_string("site_config/curtained.html", 
                    {'message':'%s' % app_config.get_curtain_message()}))
        elif active_state == choices.WEBAPP_ACTIVE_STATE_ENABLED:
            pass
        else:
            logger.debug("Website Application disabled %s - %s" % (website, app_config.application_short_name))
            raise Http404
        return the_func(*args, **kwargs)
    return _decorated


def website_template_override(the_func, template_kwarg_name="template_name"):

    def _decorated(*args, **kwargs):
        website = kwargs.get('website', None)
        # Check url pattern for template_name definition
        template_name = kwargs.get(template_kwarg_name, None)
        # Check function kwarg for template_name definition
        # Also check to make sure that the_func is a function
        #   i.e. django.contrib.syndication.views.Feed is a 
        #   valid input to a url, but is not a function 
        if website and not template_name and inspect.isfunction(the_func):
            _args, varargs, varkw, defaults = inspect.getargspec(the_func)
            result = {}
            if defaults:
                firstdefault = len(_args) - len(defaults)
            for i, arg in enumerate(_args):
                if defaults and i >= firstdefault:
                    result[arg] = defaults[i - firstdefault]
            if template_kwarg_name in result:
                template_name = result['template_name']
        if website and template_name:
            template = utils.website_override_template(template_name, website)
            kwargs.update({template_kwarg_name:template.name})
        return the_func(*args, **kwargs)
    return _decorated

