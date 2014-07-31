from __future__ import unicode_literals
import logging
from django.http import Http404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from . import choices

logger = logging.getLogger(__name__)


def enable_disable_website(the_func, config_class):

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
