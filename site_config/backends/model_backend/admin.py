from django import forms
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from site_config import registry
from site_config import utils
from . import models
from . import forms as backend_forms


class WebsiteApplicationInline(admin.TabularInline):
    def detail_link(self, obj):
        return "<a href='%s'>detail</a>" % (
            reverse('admin:site_config_websiteapplication_change', args=(obj.id,)))
    detail_link.short_description = 'Link to Detail Page'
    detail_link.allow_tags = True

    model = models.WebsiteApplication
    exclude = ['options']
    readonly_fields = ['detail_link']
    extra = 0


class WebsiteAdmin(admin.ModelAdmin):
    #inlines = [WebsiteApplicationInline,]
    list_display = ['id', 'name', 'short_name', 'active', ]
    list_editable = ['active']
    list_filter = ['active']
    prepopulated_fields = {"short_name": ("name",)}
    ordering = ['short_name']


class ApplicationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ApplicationAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_name'] = forms.ChoiceField(
            choices=registry.config_registry.get_config_list())

    class Meta:
        exclude = []
        model = models.Application


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    #inlines = [WebsiteApplicationInline,]
    list_display = ['id', 'short_name', 'active']
    list_editable = ['active']
    list_filter = ['active']
    ordering = ['short_name']


class WebsiteApplicationAdmin(admin.ModelAdmin):

    def application_active(self, obj):
        return True if obj.application.active else False
    application_active.short_description = 'App Active'
    application_active.boolean = True

    def website_active(self, obj):
        return True if obj.website.active else False
    website_active.short_description = 'Website Active'
    website_active.boolean = True

    def website_link(self, obj):
        return_value = None
        if obj:
            return_value = mark_safe("<a href='%s' onclick='return showAddAnotherPopup(this);'>Link</a>" % (
                reverse('admin:site_config_website_change', args=(obj.website.id,))))
        return return_value
    website_link.short_description = 'Link'
    website_link.allow_tags = True

    def application_link(self, obj):
        return_value = None
        if obj:
            return_value = mark_safe("<a href='%s' onclick='return showAddAnotherPopup(this);'>Link</a>" % (
                reverse('admin:site_config_application_change', args=(obj.application.id,))))
        return return_value
    application_link.short_description = 'Link'
    application_link.allow_tags = True

    list_display = [
        'id', 'website', 'website_active', 'application',
        'application_active', 'active']
    list_editable = ['active']
    list_filter = ['active', 'website', 'application']
    readonly_fields = ['website_active', 'application_active', 'website_link', 'application_link']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            [None, {
                'fields': (('website', 'website_active', 'website_link'),
                           ('application', 'application_active', 'application_link',),
                           'active', 'curtain_message', 'description', )
            }],
        ]
        form = backend_forms.website_application_formfactory(instance=obj)
        if form.config_fields:
            fieldsets.append([
                "Configuration Options", {
                    "fields": tuple(['reset_options'] + form.config_fields)
                }
            ])
        return fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        return backend_forms.website_application_formfactory(instance=obj)

    def save_model(self, request, obj, form, change):
        config_lookup = registry.config_registry.get_config_class(obj.application.short_name)
        default_config = config_lookup[1]().get_default_configs()
        if obj.id is None:
            # This branch adds default values to each config option
            config_dict = utils.config_dict_value_from_default(default_config)
        else:
            # This branch updates the current values with the form values
            config_dict = obj.get_config_options(default_config)
            config_dict.update(form.cleaned_data.get('options', {}))
        obj.set_config_options(config_dict, save=False)
        obj.save()


# If a site is using site config, the assumption is that it is using
# the model backend (this backend). However, even if a site is using
# the settings backend, it may still install the model backend and
# then set SITECONFIG_BACKEND_DEFAULT in settings.py to indicate the
# settings backend. In other words, this code could be executed even
# if the settings backend is used. In that case, however, we do not
# want the models to appear in the admin, so do not register them if
# the site is using the settings backend.
if getattr(settings, 'SITECONFIG_BACKEND_DEFAULT', False) == 'site_config.backends.settings_backend.SettingsBackend':
    pass
else:
    admin.site.register(models.Website, WebsiteAdmin)
    admin.site.register(models.Application, ApplicationAdmin)
    admin.site.register(models.WebsiteApplication, WebsiteApplicationAdmin)
