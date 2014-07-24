from django.utils.importlib import import_module


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def update_config_dict(default_config_dict, updated_config_dict):
    config_dict = default_config_dict.copy()
    if type(updated_config_dict) is dict:
        # update the value keys to be the contents of updated_config_dict
        for config_name, nested_config_dict in config_dict.items():
            if config_name in updated_config_dict and 'value' in updated_config_dict[config_name]:
                config_dict[config_name].update({'value':updated_config_dict[config_name]['value']})
    return config_dict

def config_dict_value_from_default(default_config_dict):
    config_dict = default_config_dict.copy()
    # set a default 'value' in each nested config dict
    for config_name, x in config_dict.items():
        config_dict[config_name].update({'value':config_dict[config_name]['default']})
    return config_dict