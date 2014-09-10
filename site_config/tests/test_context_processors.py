from django.test import TestCase
from django.test.utils import override_settings


import mock

from site_config import context_processors


class TestDecideBaseTemplate(TestCase):
    @override_settings(**{'SITECONFIG_BASE_TEMPLATE': "test.html"})
    def test_setting_override(self):
        """
        Verify default template used if setting not overridden
        """
        request = mock.Mock()
        request.resolver_match.kwargs.get.return_value = None
        context = context_processors.decide_base_template(request)
        self.assertEqual(context['base_template'], "test.html")

    def test_setting_default(self):
        """
        Verify setting override changes default template
        """
        request = mock.Mock()
        request.resolver_match.kwargs.get.return_value = None
        context = context_processors.decide_base_template(request)
        self.assertEqual(context['base_template'], "base_site.html")

    @mock.patch('site_config.context_processors.website_override_template')
    def test_website_pulled_from_kwargs(self, template_override_mock):
        """
        Verify website pulled from resolver_match kwargs passed to lookup
        """
        request = mock.Mock()
        request.resolver_match.kwargs.get.return_value = 'site-1'
        context_processors.decide_base_template(request)
        template_override_mock.assert_called_with(
            'base_site.html', 'site-1'
        )

    @mock.patch('site_config.context_processors.website_override_template')
    def test_template_lookup_result_returned(self, template_override_mock):
        """
        Verify result of website_override_template returned by function
        """
        mock_template = mock.Mock()
        mock_template.name = 'site-1/base_site.html'
        request = mock.Mock()
        request.resolver_match.kwargs.get.return_value = 'site-1'
        template_override_mock.return_value = mock_template
        context = context_processors.decide_base_template(request)
        self.assertEqual(
            context['base_template'], 'site-1/base_site.html'
        )
