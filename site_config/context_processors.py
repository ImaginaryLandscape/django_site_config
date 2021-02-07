from __future__ import unicode_literals
from __future__ import absolute_import
from site_config.utils import website_override_template
from site_config.backends.model_backend.models import Website
from django.conf import settings


def decide_base_template(request):
    base_name = getattr(
        settings, 'SITECONFIG_BASE_TEMPLATE', 'base_site.html'
    )
    website_obj = None
    website_name = None
    try:
        website = request.resolver_match.kwargs.get('website', None)
    except:
        website = None

    if website:
        base_name = website_override_template(base_name, website).name
    else:
        parts = [part for part in request.path.split('/') if part != ""]
        if len(parts) > 0:
            website = parts[0]
            base_name = website_override_template(base_name, website).name

    if website:
        try:
            website_obj = Website.objects.get(short_name=website)
            website_name = website_obj.name
        except Website.DoesNotExist as e:
            website_obj = None

    return {
        'base_template': base_name,
        'website_shortname': website,
        'website_name': website_name,
        'website_obj': website_obj,
        'website': website_obj
    }
