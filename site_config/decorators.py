from __future__ import unicode_literals
import logging
from django.http import Http404
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from . import choices

logger = logging.getLogger(__name__)


def determine_website(the_func, config_class):

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
