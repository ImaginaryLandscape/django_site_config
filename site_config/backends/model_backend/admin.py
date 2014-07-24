from django.contrib import admin
from django import forms
from site_config import settings
from . import models


class WebSiteApplicationInline(admin.StackedInline):
    model = models.WebSiteApplication
    exclude = ['options']
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
    list_display=['id', 'website', 'application', 'active',]
    list_editable=['active',]
    list_filter=['active']

    def get_form(self, request, obj=None, **kwargs):
        meta_options = {
             "model":models.WebSiteApplication, 
             'exclude':['options',],
        }
        properties = {"Meta": type('Meta', (), meta_options)}
        
        # only add config options for existing objects
        if obj:
            # lookup the configuration class for this object, based on the application slug
            config_lookup = settings.config_registry.get_config_class(obj.application.slug)
            if config_lookup:
                config_class = config_lookup[1](website=obj.website.slug)
                for config_name, value in config_class.get_configs().items():
                    properties.update( {
                        config_name: value['field'](label=config_name,
                                    help_text=value['help'], 
                                    initial=value['default'], required=False),
                    })

        form = type('WebSiteApplicationAdminForm', (forms.ModelForm,), properties)
    
        return form


admin.site.register(models.WebSite, WebSiteAdmin)
admin.site.register(models.Application, ApplicationAdmin)
admin.site.register(models.WebSiteApplication, WebSiteApplicationAdmin)

