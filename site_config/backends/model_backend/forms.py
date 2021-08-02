import importlib
import logging
from django import forms
from site_config import registry, utils
from . import models

logger = logging.getLogger(__name__)


def website_application_formfactory(instance=None):
    config_class = None
    meta_options = {
        "model": models.WebsiteApplication,
        'exclude': ['options', ],
    }
    properties = {"Meta": type('Meta', (), meta_options)}
    # for deserialization, we need to know which fields are config fields
    config_fields = []
    # only add config options for existing objects
    if instance:
        # lookup the configuration class for this object,
        # based on the application short_name
        config_lookup = registry.config_registry.get_config_class(
            instance.application.short_name
        )
        if config_lookup:
            config_class = config_lookup[1](
                website=instance.website.short_name
            )
            config_fields = []
            for config_name, lookup_dict in config_class.get_configs().items():
                config_fields.append(config_name)
                field_class = utils.import_module_attr(lookup_dict['field'])
                kwargs = dict(
                    label=config_name,
                    help_text="%s Default: %s" % (lookup_dict.get('help', ''),
                                                  lookup_dict['default']),
                    initial=lookup_dict['value'],
                    required=False
                )
                if hasattr(field_class, 'choices') and \
                        'choices' in lookup_dict:
                    kwargs.update(
                        {'choices': lookup_dict.get('choices', None)}
                    )
                if hasattr(field_class, "queryset") and \
                        'queryset' in lookup_dict:
                    func = import_helper(lookup_dict.get('queryset'))
                    kwargs.update(
                        {'queryset': func()}
                    )
                properties.update({
                    config_name: field_class(**kwargs),
                })
            properties.update(
                {
                    'reset_options': forms.BooleanField(
                        label="Reset to Defaults",
                        required=False, initial=False
                    ),
                }
            )

    def clean_form(self):
        cleaned_data = super(self.__class__, self).clean()
        if instance and config_class:
            if cleaned_data.get('reset_options'):
                cleaned_data['options'] = utils.config_dict_value_from_default(
                    config_class.get_configs())
            else:
                cleaned_configs = {}
                for k, v in cleaned_data.items():
                    if k in config_fields:
                        cleaned_configs.update(
                            {k: {'value': cleaned_data.pop(k)}}
                        )
                cleaned_data['options'] = utils.update_config_dict(
                    config_class.get_configs(), cleaned_configs)
        return cleaned_data
    properties.update(
        {"config_fields": sorted(config_fields), 'clean': clean_form})
    form = type(
        'WebsiteApplicationAdminForm', (forms.ModelForm, ), properties
    )
    return form


def import_helper(name):
    class_data = name.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_str)
