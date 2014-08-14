import mock
# from copy import deepcopy
# from django.conf.urls import patterns, url, include
from django.http import Http404
from django.test import TestCase
from django.test.utils import override_settings
from site_config import decorators
from .test_modelbackend_basic_usage import ModelsBaiscMixin
from . import lib


@override_settings(**lib.settings_overrides)
class TestDecorators(ModelsBaiscMixin, lib.SiteConfigMixin, TestCase):
    def helper_func(*args, **kwargs):
        if 'template_name' in kwargs.keys() and kwargs['template_name'] == []:
            return False
        return True

    class User:
        def __init__(self, authed, superuser):
            self.authed = authed
            self.is_superuser = superuser

        def is_authenticated(self):
            return self.authed

    def setUp(self):
        self.load_config()
        self.load_models()
        self.site_config.registry.config_registry.register(self.MyAppSiteConfig)

    def _set_model_active_state(self, website, application, webapp):
        self.Website.objects.filter().update(active=website)
        self.Application.objects.filter().update(active=application)
        self.WebsiteApplication.objects.filter().update(active=webapp)

    def test_enable_disable_website__enabled(self):
        self._set_model_active_state(True, True, "enabled")
        decorated_func = decorators.enable_disable_website(self.helper_func, self.MyAppSiteConfig)
        context = {'website': self.site1_short_name}
        self.assertTrue(decorated_func(**context))

    def test_enable_disable_website__disabled(self):
        self._set_model_active_state(True, True, "disabled")
        decorated_func = decorators.enable_disable_website(self.helper_func, self.MyAppSiteConfig)
        context = {'website': self.site1_short_name}
        try:
            decorated_func(**context)
        except Http404:
            pass

    def test_enable_disable_website__curtained_not_superuser(self):
        self._set_model_active_state(True, True, "curtained")
        decorated_func = decorators.enable_disable_website(self.helper_func, self.MyAppSiteConfig)
        context = {'website': self.site1_short_name}
        mock_user = mock.Mock()
        mock_user.user = self.User(False, False)
        args = [mock_user, ]
        self.assertTrue('maintenance' in decorated_func(*args, **context).content)

    def test_enable_disable_website__curtained_is_superuser_authed(self):
        self._set_model_active_state(True, True, "curtained")
        decorated_func = decorators.enable_disable_website(self.helper_func, self.MyAppSiteConfig)
        context = {'website': self.site1_short_name}
        mock_user = mock.Mock()
        mock_user.user = self.User(True, True)
        args = [mock_user, ]
        self.assertTrue(decorated_func(*args, **context))

    def test_enable_disable_website__curtained_is_superuser_unauthed(self):
        self._set_model_active_state(True, True, "curtained")
        decorated_func = decorators.enable_disable_website(self.helper_func, self.MyAppSiteConfig)
        context = {'website': self.site1_short_name}
        mock_user = mock.Mock()
        mock_user.user = self.User(False, True)
        args = [mock_user, ]
        self.assertTrue('maintenance' in decorated_func(*args, **context).content)

    def test_enable_disable_website__curtained_not_superuser_authed(self):
        self._set_model_active_state(True, True, "curtained")
        decorated_func = decorators.enable_disable_website(self.helper_func, self.MyAppSiteConfig)
        context = {'website': self.site1_short_name}
        mock_user = mock.Mock()
        mock_user.user = self.User(True, False)
        args = [mock_user, ]
        self.assertTrue('maintenance' in decorated_func(*args, **context).content)

#    def test_website_template_override__default(self):
#        decorated_func = decorators.website_template_override(self.helper_func)
#        context = {'website': self.site1_short_name}
#        self.assertTrue(decorated_func(**context))

'''
    @mock.patch("site_config.decorators.utils.website_override_template")
    def test_website_template_override__override(self, override_template):
        override_template.return_value = ['app4.html']
        decorated_func = decorators.website_template_override(self.helper_func)
        context = {'website': self.site1_short_name, 'template_name': ['apps.html']}
        self.assertTrue(decorated_func(**context))
'''
