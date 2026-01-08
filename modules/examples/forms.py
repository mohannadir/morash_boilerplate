from django import forms
from django.utils.translation import gettext_lazy as _

from modules.forms import FormWithPlaceholders

class SendTestEmailForm(FormWithPlaceholders):
    to_email = forms.EmailField(label=_('To Email Address'))

    class Meta:
        placeholders = {
            'to_email' : _('Fill in your email address'),
        }

class ConsumeCreditForm(FormWithPlaceholders):
    amount = forms.IntegerField(label=_('Amount'))
    action = forms.CharField(label=_('Action'))

    class Meta:
        placeholders = {
            'amount' : _('Amount of credits to consume'),
            'action' : _('The reason for consuming the credits'),
        }

class GenerateImageForm(FormWithPlaceholders):
    prompt = forms.CharField(label=_('Prompt'), widget=forms.Textarea)
    size = forms.ChoiceField(label=_('Size'), choices=[('1024x1024', '1024x1024'), ('1024x1792', '1024x1792'), ('1792x1024', '1792x1024')])
    quality = forms.ChoiceField(label=_('Quality'), choices=[('standard', 'Standard'), ('hd', 'HD')])

    class Meta:
        placeholders = {
            'prompt' : _('The prompt to generate the image from'),
            'size' : _('The size of the image to generate'),
            'quality' : _('The quality of the image to generate'),
        }