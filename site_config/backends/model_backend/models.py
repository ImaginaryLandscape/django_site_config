from __future__ import unicode_literals
import logging
from jsonfield import JSONField
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models.signals import post_save
from site_config import utils

logger = logging.getLogger(__name__)

@python_2_unicode_compatible
class WebSite(models.Model):
    
    name = models.CharField(max_length=64, 
        help_text="Enter a descriptive name for this website.")
    slug = models.SlugField(max_length=64, unique=True, 
        help_text="This must be a unique name using only "
                  "letter, numbers, hyphens, and underscores.")
    active = models.BooleanField(default=False, 
        help_text="Enable or disable the entire website.")
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'site_config'
        verbose_name = "Website"
        verbose_name_plural = "Websites"

    def __str__(self):
        return "%s (%s)" % (self.name, self.slug)


@python_2_unicode_compatible
class Application(models.Model):

    slug = models.SlugField(max_length=64, unique=True,
        help_text="This must be a unique name using only "
                  "letter, numbers, hyphens, and underscores.")
    active = models.BooleanField(default=False, 
        help_text="Enable or disable the entire application.")
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'site_config'
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return "%s" % (self.slug)


class WebSiteApplicationQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(active=True)

    def website_applications(self, website_slug, application_slug):
        return self.filter(
                        application__slug=application_slug, 
                        website__slug=website_slug, )


class WebSiteApplicationManager(models.Manager):
    
    def get_queryset(self):
        return WebSiteApplicationQuerySet(self.model, using=self._db)
    
    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)
        

@python_2_unicode_compatible
class WebSiteApplication(models.Model):
    
    website = models.ForeignKey('site_config.WebSite')
    application = models.ForeignKey('site_config.Application')
    
    active = models.BooleanField(default=False, 
        help_text="Activates or deactivates this website application combination. "
        "In order for this to be active, both the corresponding "
        "website and application must also be active.")
    description = models.TextField(blank=True, null=True)

    options = JSONField(blank=True, null=True)
    
    objects = WebSiteApplicationManager()
    
    def get_config_options(self, default_config_dict):
        return utils.update_config_dict(default_config_dict, self.options)

    def set_config_options(self, config_dict, save=True):
        self.options = config_dict
        if save:
            self.save()

    def is_active(self):
        return_value =  self.website.active & self.application.active & self.active
        return return_value

    class Meta:
        app_label = 'site_config'
        verbose_name = "Website Application"
        verbose_name_plural = "Websites Applications"
        unique_together = (('website', 'application'),)

    def __str__(self):
        return "%s (%s)" % (self.website, self.application)
