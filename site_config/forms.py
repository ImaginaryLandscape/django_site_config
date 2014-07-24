from __future__ import unicode_literals
from django import forms

class SiteConfigValueForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SiteConfigValueForm, self).__init__(*args, **kwargs)
        for name, (default, help_text) in settings.CONFIG.items():
            field_class, kwargs = FIELDS[type(default)]
            self.fields[name] = field_class(label=name, **kwargs)

    def save(self):
        for name in self.cleaned_data:
            setattr(config, name, self.cleaned_data[name])