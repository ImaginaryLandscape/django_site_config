from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from site_config import settings
from . import models


class WebSiteApplicationInline(admin.StackedInline):
    def detail_link(self, obj):
        return "<a href='%s'>detail</a>" % (reverse('admin:site_config_websiteapplication_change', args=(obj.id,)))
    detail_link.short_description = 'Link to Detail Page'
    detail_link.allow_tags = True
    
    model = models.WebSiteApplication
    exclude = ['options']
    readonly_fields = ['detail_link']
    extra = 0


class WebSiteAdmin(admin.ModelAdmin):
    inlines = [WebSiteApplicationInline,]
    list_display=['id', 'name', 'slug', 'active', ]
    list_editable = ['active',]
    list_filter=['active']
    prepopulated_fields = {"slug": ("name",)}


class ApplicationAdminForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ApplicationAdminForm, self).__init__(*args, **kwargs)
        self.fields['slug'] = forms.ChoiceField(choices=settings.config_registry.get_config_list())
    
    class Meta:
        model = models.Application

class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    inlines = [WebSiteApplicationInline,]    
    list_display=['id', 'name', 'slug', 'active',]
    list_editable=['active',]
    list_filter=['active']
    prepopulated_fields = {"slug": ("name",)}


class WebSiteApplicationAdmin(admin.ModelAdmin):

    def application_active(self, obj):
        return True if obj.application.active else False
    application_active.short_description = 'App Active'
    application_active.boolean = True

    def website_active(self, obj):
        return True if obj.website.active else False
    website_active.short_description = 'Website Active'
    website_active.boolean = True

    list_display=['id', 'website', 'website_active', 'application', 'application_active', 'active',]
    list_editable=['active',]
    list_filter=['active', 'website', 'application']
    readonly_fields = ['website_active', 'application_active' ]

    def __init__(self, *args, **kwargs):
        super(WebSiteApplicationAdmin, self).__init__(*args, **kwargs)
        self.fieldsets = [
            [None, {
                'fields': (('website', 'website_active'), 
                           ('application', 'application_active',),
                           'active', 'description', )
            }],
        ]

    def get_form(self, request, obj=None, **kwargs):
        meta_options = {
             "model":models.WebSiteApplication, 
             'exclude':['options',],
        }
        properties = {"Meta": type('Meta', (), meta_options)}

        self.fieldsets = [
            [None, {
                'fields': (('website', 'website_active'), 
                           ('application', 'application_active',),
                           'active', 'description', )
            }],
        ]

        # only add config options for existing objects
        if obj:
            # lookup the configuration class for this object, based on the application slug
            config_lookup = settings.config_registry.get_config_class(obj.application.slug)
            if config_lookup:
                config_class = config_lookup[1](website=obj.website.slug)
                config_fields = []
                for config_name, lookup_dict in config_class.get_configs().items():
                    config_fields.append(config_name)
                    properties.update( {
                        config_name: lookup_dict['field'](label=config_name,
                                    help_text="%s Default: %s" % (lookup_dict['help'], lookup_dict['value']), 
                                    initial=lookup_dict['value'], required=False),
                    })
                # for deserialization, we need to know which fields are config fields
                properties.update({"config_fields": config_fields})
                self.fieldsets.append(["Configuration Options", {"fields":config_fields}],)


        form = type('WebSiteApplicationAdminForm', (forms.ModelForm,), properties)
    
        return form


admin.site.register(models.WebSite, WebSiteAdmin)
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.WebSiteApplication, WebSiteApplicationAdmin)

