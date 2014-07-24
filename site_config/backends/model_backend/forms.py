from django import forms
from site_config import settings, utils
from . import models


def website_application_formfactory(instance=None):
    config_class = None
    meta_options = {
         "model":models.WebSiteApplication, 
         'exclude':['options',],
    }
    properties = {"Meta": type('Meta', (), meta_options)}
    # for deserialization, we need to know which fields are config fields
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
                field_class = utils.import_module_attr(lookup_dict['field'])
                properties.update( {
                    config_name: field_class(label=config_name,
                                help_text="%s Default: %s" % (
                                    lookup_dict.get('help', ''), lookup_dict['default']), 
                                initial=lookup_dict['value'], required=False),
                })
    
    def clean_form(self):
        cleaned_data = self.cleaned_data
        if instance and config_class:
            cleaned_configs = {}
            for k,v in cleaned_data.items():
                if k in config_fields:
                    cleaned_configs.update({k:{'value':cleaned_data.pop(k)}})
            cleaned_data['options'] = utils.update_config_dict(config_class.get_configs(), cleaned_configs)
            #raise forms.ValidationError("%s" % cleaned_data)
        return cleaned_data
    
    properties.update({"config_fields": config_fields, 'clean':clean_form})
    form = type('WebSiteApplicationAdminForm', (forms.ModelForm,), properties)
    return form