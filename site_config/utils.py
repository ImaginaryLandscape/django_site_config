import os
from copy import deepcopy
from django.db.models.query import QuerySet
from importlib import import_module
from django.template.loader import select_template


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def id_for_item(item):
    if hasattr(item, 'id'):
        return item.id
    else:
        return item


def update_config_dict(default_config_dict, updated_config_dict):
    """
    Takes a config_dict and updates the values in the nested meta
    dicts with the values provided in the updated_config_dict.

    INPUT
     default_config_dict = see the output of
          site_config.get_default_configs()
     updated_config_dict = {'TEST_A': {"value": "1234"},
                           'TEST_B': {"value": 1},
                           }
    OUTPUT
    i.e.
    {"TEST_A": {"default": ...,
                "field": ...,
                "help": ...,
                "value":"1234",
                }
     "TEST_B": {"default": ...,
                "field": ...,
                "help": ...,
                "value":1,
                }
    }
    """
    config_dict = deepcopy(default_config_dict)
    if type(updated_config_dict) is dict:
        # update the value keys to be the contents of updated_config_dict
        for config_name, nested_config_dict in config_dict.items():
            if config_name in updated_config_dict and \
                    'value' in updated_config_dict[config_name]:
                if 'queryset' in config_dict[config_name]:
                    """
                    If it is a list of queryset, make sure we serialize as
                    list of integers to prevent JSON serialization problems.

                    If it is an object with an id, make sure we serialize as
                    the id of the object.
                    """
                    val = updated_config_dict[config_name]['value']
                    if isinstance(val, list) or isinstance(val, QuerySet):
                        val = [id_for_item(v) for v in val]
                    else:
                        val = id_for_item(val)
                    config_dict[config_name].update(
                        {'value': val}
                    )
                else:
                    config_dict[config_name].update(
                        {'value': updated_config_dict[config_name]['value']}
                    )
    return config_dict


def config_dict_value_from_default(default_config_dict):
    """
    Takes a config_dict and updates the "value" attribute of
    all of the nested "meta" dicts to the value of the corresponding
    "default" attribute.

    INPUT
     default_config_dict = see the output of
          site_config.get_default_configs()
    """

    new_config_dict = deepcopy(default_config_dict)
    # set a default 'value' in each nested config dict
    for config_name, x in new_config_dict.items():
        new_config_dict[config_name].update(
            {'value': new_config_dict[config_name]['default']})
    return new_config_dict


def website_override_template(template_name, website):
    """
    Tries to look for a template on the template path named
    [website]/[template_name], then falls back to looking
    for a template at [template_name].  If neither exist,
    this raises a TempateDoesNotExist error.
    """
    website_template_name = os.path.join(website, template_name)
    template_obj = select_template((website_template_name, template_name,))
    # Prior to Django 1.8, the above returns a template.
    # With Django 1.8, we need to unwrap the template from the above.
    if hasattr(template_obj, 'template'):
        template_obj = template_obj.template
    return template_obj


class WebsiteOverrideTemplateViewMixin(object):
    """
    Mix this class into a CBV where you want to
    provide a means for the website to override the
    template. The self.website attribute must be
    set in order for this mixin to override a template.

    Tries to look for a template on the template path named
    [self.website]/[template_name], then falls back to looking
    for a template at [template_name].  If neither exist,
    this raises a TempateDoesNotExist error.
    """
    def get_template_names(self):
        templates = super(
            WebsiteOverrideTemplateViewMixin, self
        ).get_template_names()
        website = getattr(self, 'website', None)
        if website is None:
            website = self.kwargs.get('website', None)
        if website:
            templates = [os.path.join(website, self.template_name)] + templates
        return templates
