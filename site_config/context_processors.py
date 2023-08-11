from site_config.utils import website_override_template
from site_config.backends.model_backend.models import Application, Website, WebsiteApplication
from django.conf import settings


def get_app_obj(request):
    app_names = request.resolver_match.app_names
    if app_shortname := app_names[0] if app_names else None:
        try:
            app_obj = Application.objects.get(short_name=app_shortname)
        except Application.DoesNotExist as e:
            return None
        return app_obj
    return None

def get_website_obj(request):
    if website_shortname := request.resolver_match.kwargs.get('website'):
        try:
            website_obj = Website.objects.get(short_name=website_shortname)
        except Website.DoesNotExist as e:
            return None
        return website_obj
    return None

def decide_base_template(request):
    if website_obj := get_website_obj(request):
        base_template = getattr(settings, 'SITECONFIG_BASE_TEMPLATE', 'base_site.html')
        base_template = website_override_template(base_template, website_obj.short_name).name
        return {
            'base_template': base_template,
            'website_shortname': website_obj.short_name,
            'website_name': website_obj.name,
            'website_obj': website_obj
        }
    # else
    return {}


#def decide_base_template(request):
#    base_template = getattr(
#        settings, 'SITECONFIG_BASE_TEMPLATE', 'base_site.html'
#    )
#    website_obj = None
#    website_name = None
#    try:
#        website_shortname = request.resolver_match.kwargs.get('website', None)
#    except:
#        website_shortname = None
#
#    if website_shortname:
#        base_template = website_override_template(base_template, website_shortname).name
#    else:
#        parts = [part for part in request.path.split('/') if part != ""]
#        if len(parts) > 0:
#            website_shortname = parts[0]
#            base_template = website_override_template(base_template, website_shortname).name
#
#    if website_shortname:
#        try:
#            website_obj = Website.objects.get(short_name=website_shortname)
#            website_name = website_obj.name
#        except Website.DoesNotExist as e:
#            website_obj = None
#
#    return {
#        'base_template': base_template,
#        'website_shortname': website_shortname,
#        'website_name': website_name,
#        'website_obj': website_obj
#    }


def add_site_specific_options(request):
    if website_obj := get_website_obj(request):
        if app_obj := get_app_obj(request):
            try:
                wa = WebsiteApplication.objects.get(website=website_obj, application=app_obj)
            except WebsiteApplication.DoesNotExist as e:
                return {}
            options_dict = {}
            for option in wa.options:
                options_dict[option] = wa.options[option].get("value") or wa.options[option].get("default")
            #options_dict = {option: wa.options[option].get("value") or wa.options[option].get("default") for option in wa.options}
            return {"siteconfig_options": options_dict}
    return {}
