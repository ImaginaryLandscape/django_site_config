from django import forms
import site_config


class BarConfig(site_config.SiteConfigBase):

    application_short_name = "bar"
    application_verbose_name = "Bar App"

    def get_default_configs(self):
        return {'BAR_EMAIL': {'default': "joe@exampe.com",
                              'field': 'django.forms.CharField',
                              'help': 'Test A help text.'},
                "BAR_NUM": {'default': 1,
                            'field': 'django.forms.IntegerField',
                            'help': 'Enter a number.'},
                "BAR_CHAR": {'default': "b",
                             'field': 'django.forms.ChoiceField',
                             'help': 'Test B help text.',
                             'choices': (('a', "A choice"), ("b", "B Choice"),)},
                }

site_config.registry.config_registry.register(BarConfig)
