from django.forms.renderers import DjangoTemplates
from django import forms

class FormRenderer(DjangoTemplates):
    field_template_name = "components/forms/field_group.html"

class ModelFormWithPlaceholders(forms.ModelForm):
    """ This form class allows you to specify placeholders for fields in the Meta class. """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.Meta.placeholders:
            for field_name, placeholder in self.Meta.placeholders.items():
                self.fields[field_name].widget.attrs['placeholder'] = placeholder
        else:
            for field_name, field in self.fields.items():
                field.widget.attrs['placeholder'] = field.label

class FormWithPlaceholders(forms.Form):
    """ This form class allows you to specify placeholders for fields in the Meta class. """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.Meta.placeholders:
            for field_name, placeholder in self.Meta.placeholders.items():
                self.fields[field_name].widget.attrs['placeholder'] = placeholder
        else:
            for field_name, field in self.fields.items():
                field.widget.attrs['placeholder'] = field.label