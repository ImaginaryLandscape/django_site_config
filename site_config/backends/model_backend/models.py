from __future__ import unicode_literals
from jsonfield import JSONField
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models.signals import post_save


@python_2_unicode_compatible
class WebSite(models.Model):
    
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'site_config'
        verbose_name = "Website"
        verbose_name_plural = "Websites"

    def __str__(self):
        return "%s (%s)" % (self.name, self.slug)


@python_2_unicode_compatible
class Application(models.Model):

    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'site_config'
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return "%s (%s)" % (self.name, self.slug)


class WebSiteApplicationQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(active=True)

    def active_website_applications(self, website_slug, application_slug):
        return self.active().filter(
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
    
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    options = JSONField(blank=True, null=True)
    
    objects = WebSiteApplicationManager()
    
    def get_config_option(self, key, default):
        return_value  = default
        if self.options:
            return_value = self.options.get(key, default)
        return return_value
    
    class Meta:
        app_label = 'site_config'
        verbose_name = "Website Application"
        verbose_name_plural = "Websites Applications"
        unique_together = ['website', 'application']

    def __str__(self):
        return "%s (%s)" % (self.website, self.application)
