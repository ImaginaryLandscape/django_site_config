from __future__ import absolute_import
import unittest

import mock

from site_config.backends.model_backend import admin, models


class TestWAAdmin(unittest.TestCase):
    @mock.patch('site_config.backends.model_backend.admin.registry')
    def test_save_model_no_id(self, registry_mock):
        """
        Assert default config used if obj is new (has no id)
        """
        wa_admin = admin.WebsiteApplicationAdmin(
            models.WebsiteApplication,
            mock.MagicMock()
        )
        obj = mock.Mock()
        obj.application.short_name = 'test'
        obj.id = None

        config = mock.MagicMock()
        config.return_value.get_default_configs.return_value = {'TEST': {'default': 'value',
                                                                         'field': 'django.forms.CharField',
                                                                         'help': 'A test field'}}
        config_list = ("Test", config)
        registry_mock.config_registry.get_config_class.return_value = (
            config_list
        )

        wa_admin.save_model(None, obj, None, None)

        registry_mock.config_registry.get_config_class.assert_called_with(
            'test'
        )
        obj.set_config_options.assert_called_with(
            {'TEST': {'default': 'value',
                      'field': 'django.forms.CharField',
                      'help': 'A test field',
                      'value': 'value'}},
            save=False
        )
        obj.save.assert_called()

    @mock.patch('site_config.backends.model_backend.admin.registry')
    def test_save_model_with_id(self, registry_mock):
        """
        Assert config returned from form is used if obj is not new (has id)
        """
        wa_admin = admin.WebsiteApplicationAdmin(
            models.WebsiteApplication,
            mock.MagicMock()
        )
        obj = mock.Mock()
        obj.id = 1

        form = mock.Mock()
        form.cleaned_data.get.return_value = {'key': 'val2'}

        wa_admin.save_model(None, obj, form, None)

        obj.set_config_options.assert_called_with({'key': 'val2'}, save=False)

        obj.save.assert_called()
