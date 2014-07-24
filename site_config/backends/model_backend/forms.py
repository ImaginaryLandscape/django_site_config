from django import forms
from site_config import settings
from . import models


def website_application_formfactory(instance=None):
    meta_options = {
         "model":models.WebSiteApplication, 
         'exclude':['options',],
    }
    properties = {"Meta": type('Meta', (), meta_options)}
    config_fields = []
    # only add config options for existing objects
    if instance:
        # lookup the configuration class for this object, based on the application slug
        config_lookup = settings.config_registry.get_config_class(instance.application.slug)
        if config_lookup:
            config_class = config_lookup[1](website=instance.website.slug)
            config_fields = []
            for config_name, lookup_dict in config_class.get_configs().items():
                config_fields.append(config_name)
                properties.update( {
                    config_name: lookup_dict['field'](label=config_name,
                                help_text="%s Default: %s" % (
                                    lookup_dict.get('help', ''), lookup_dict['value']), 
                                initial=lookup_dict['value'], required=False),
                })
    # for deserialization, we need to know which fields are config fields
    properties.update({"config_fields": config_fields})
    form = type('WebSiteApplicationAdminForm', (forms.ModelForm,), properties)
    return form