from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from site_config import settings
from . import models
from . import forms as backend_forms


class WebsiteApplicationInline(admin.TabularInline):
    def detail_link(self, obj):
        return "<a href='%s'>detail</a>" % (reverse('admin:site_config_websiteapplication_change', args=(obj.id,)))
    detail_link.short_description = 'Link to Detail Page'
    detail_link.allow_tags = True
    
    model = models.WebsiteApplication
    exclude = ['options']
    readonly_fields = ['detail_link']
    extra = 0


class WebsiteAdmin(admin.ModelAdmin):
    inlines = [WebsiteApplicationInline,]
    list_display=['id', 'name', 'short_name', 'active', ]
    list_editable = ['active',]
    list_filter=['active']
    prepopulated_fields = {"short_name": ("name",)}


class ApplicationAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ApplicationAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_name'] = forms.ChoiceField(choices=settings.config_registry.get_config_list())
    
    class Meta:
        model = models.Application

class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    #inlines = [WebsiteApplicationInline,]    
    list_display=['id', 'short_name', 'active',]
    list_editable=['active',]
    list_filter=['active']


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
            return_value =  "<a href='%s' onclick='return showAddAnotherPopup(this);'>Link</a>" % (
                reverse('admin:site_config_website_change', args=(obj.website.id,)))
        return return_value
    website_link.short_description = 'Link'
    website_link.allow_tags = True

    def application_link(self, obj):
        return_value = None
        if obj:
            return_value =  "<a href='%s' onclick='return showAddAnotherPopup(this);'>Link</a>" % (
                reverse('admin:site_config_application_change', args=(obj.application.id,)))
        return return_value
    application_link.short_description = 'Link'
    application_link.allow_tags = True

    list_display=['id', 'website', 'website_active', 'application', 'application_active', 'active',]
    list_editable=['active',]
    list_filter=['active', 'website', 'application']
    readonly_fields = ['website_active', 'application_active', 'website_link', 'application_link']

    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = [
            [None, {
                'fields': (('website', 'website_active', 'website_link'), 
                           ('application', 'application_active', 'application_link',),
                           'active', 'description', )
            }],
        ]

        form = backend_forms.website_application_formfactory(instance=obj)
        if form.config_fields:
            self.fieldsets.append(["Configuration Options", {"fields":['reset_options',] + form.config_fields}],)
        return form

    def save_model(self, request, obj, form, change):
        obj.set_config_options(form.cleaned_data.get('options', {}), save=False)
        obj.save()


admin.site.register(models.Website, WebsiteAdmin)
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.WebsiteApplication, WebsiteApplicationAdmin)

