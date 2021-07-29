import logging
from jsonfield import JSONField
import django
from django.db import models
from site_config import utils, choices

logger = logging.getLogger(__name__)


class Website(models.Model):

    name = models.CharField(
        max_length=64,
        help_text="Enter a descriptive name for this website.")
    short_name = models.SlugField(
        max_length=64, unique=True,
        help_text="This must be a unique name using only "
                  "letter, numbers, hyphens, and underscores.")
    active = models.BooleanField(
        default=False,
        help_text="Enable or disable the entire website.")
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'site_config'
        verbose_name = "Website"
        verbose_name_plural = "Websites"
        ordering = ['short_name']

    def __str__(self):
        return "%s (%s)" % (self.name, self.short_name)


class Application(models.Model):

    short_name = models.SlugField(
        max_length=64, unique=True,
        help_text="This must be a unique name using only "
                  "letter, numbers, hyphens, and underscores.")
    active = models.BooleanField(
        default=False,
        help_text="Enable or disable the entire application.")
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'site_config'
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ['short_name']

    def __str__(self):
        return "%s" % (self.short_name)


# Why was this made like this? It looks like we're creating a custom
# Manager object so apps can call "objects.website_applications()"
# instead of the normal "objects.filter( ... )" etc. I guess that's
# a nice convenience, but if it means overriding "__getattr__()", is
# it worth it? That pattern leads to trouble, at least in Dj. 1.11.

# I don't understand why this was made this way, but I'm commenting
# out these customizations. Methods in "__init__.py", will just have
# to call `WebsiteApplication.objects.filter(website__short_name= ...)`
# (etc) like you do with every other Manager object.
#
# If I've overlooked something and things don't work right anymore,
# I'm sorry. Hopefully I can fix it better later. - NTT
#
#class WebsiteApplicationQuerySet(models.query.QuerySet):
#
#    def active(self):
#        return self.filter(active=True)
#
#    def website_applications(self, website_short_name, application_short_name):
#        return self.filter(
#                        application__short_name=application_short_name,
#                        website__short_name=website_short_name, )


#class WebsiteApplicationManager(models.Manager):
#
#    def get_queryset(self):
#        return WebsiteApplicationQuerySet(self.model, using=self._db)
#
#    if django.VERSION < (1, 6):
#        get_query_set = get_queryset
#
##    def __getattr__(self, attr, *args):
##        try:
##            return getattr(self.__class__, attr, *args)
##        except AttributeError:
##            get_queryset = (
##                self.get_query_set
##                if hasattr(self, 'get_query_set')
##                else self.get_queryset)
##            return getattr(get_queryset(), attr, *args)


class WebsiteApplication(models.Model):

    website = models.ForeignKey('site_config.Website', on_delete=models.CASCADE)
    application = models.ForeignKey('site_config.Application', on_delete=models.CASCADE)

    active = models.CharField(
        max_length=20,
        default=choices.WEBAPP_ACTIVE_STATE_DISABLED,
        choices=choices.WEBAPP_ACTIVE_STATES,
        help_text="Activates, curtains or deactivates this website application "
        "combination. In order for this to be active, both the corresponding "
        "website and application must also be active.  Curtained sites can "
        "only be viewed by superusers.")
    description = models.TextField(blank=True, null=True)
    curtain_message = models.TextField(
        blank=True, null=True,
        default="This site is undergoing scheduled maintenance."
                "Thank you for your patience.",
        help_text="Specify a message that should be displayed "
                  "when the site is in the curtained state.")
    options = JSONField(blank=True, null=True)

# See comments above for why I deactivated this custom manager - NTT.
#    objects = WebsiteApplicationManager()

    def get_config_options(self, default_config_dict):
        return utils.update_config_dict(default_config_dict, self.options)

    def set_config_options(self, config_dict, save=True):
        self.options = config_dict
        if save:
            self.save()

    def active_status(self):
        return_value = choices.WEBAPP_ACTIVE_STATE_DISABLED
        if self.website.active and self.application.active and \
           self.active in [choices.WEBAPP_ACTIVE_STATE_ENABLED,
                           choices.WEBAPP_ACTIVE_STATE_CURTAINED]:
            return_value = self.active
        return return_value

    def get_curtain_message(self):
        return self.curtain_message

    class Meta:
        app_label = 'site_config'
        verbose_name = "Website Application"
        verbose_name_plural = "Websites Applications"
        unique_together = (('website', 'application'),)

    def __str__(self):
        return "%s (%s)" % (self.website, self.application)
