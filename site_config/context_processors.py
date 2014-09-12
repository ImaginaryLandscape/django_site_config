from __future__ import unicode_literals
from site_config.utils import website_override_template
from django.conf import settings


def decide_base_template(request):
    base_name = getattr(
        settings, 'SITECONFIG_BASE_TEMPLATE', 'base_site.html'
    )
    website = request.resolver_match.kwargs.get('website', None)
    if website:
        base_name = website_override_template(base_name, website).name
    return {
        'base_template': base_name
    }
