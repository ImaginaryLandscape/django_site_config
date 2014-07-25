from __future__ import unicode_literals
from copy import deepcopy
from django.utils.importlib import import_module


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


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
            if config_name in updated_config_dict and 'value' in updated_config_dict[config_name]:
                config_dict[config_name].update({'value':updated_config_dict[config_name]['value']})
    return config_dict


def config_dict_value_from_default(default_config_dict):
    new_config_dict = deepcopy(default_config_dict)
    # set a default 'value' in each nested config dict
    for config_name, x in new_config_dict.items():
        new_config_dict[config_name].update({'value':new_config_dict[config_name]['default']})
    return new_config_dict