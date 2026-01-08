from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _

from modules.forms import ModelFormWithPlaceholders

from django.contrib.auth import get_user_model

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Email address')
        self.fields['username'].widget.attrs['placeholder'] = _('Your email address')
        self.fields['password'].widget.attrs['placeholder'] = _('Your password')

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

        labels = {
            'username': _('Email address'),
        }

        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Your email address')
        self.fields['password1'].widget.attrs['placeholder'] = _('Your password')
        self.fields['password2'].widget.attrs['placeholder'] = _('Repeat your password')

    def clean_username(self):
        username = self.cleaned_data['username']

        if get_user_model().objects.filter(email=username).exists():
            raise forms.ValidationError(_('This email address is already in use.'))
        
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)

        # Set the email as the username
        user.email = self.cleaned_data['username']

        # Deactivate the user until they verify their email
        user.is_active = False

        if commit:
            user.save()
            user.send_activation_email()
        
        return user
    
class UserForgotPasswordForm(forms.Form):

    email = forms.EmailField(
        label=_('Email address'),
        help_text=_('Enter the email address associated with your account. If it exists, we will send you an email to reset your password.'),
        widget=forms.EmailInput(attrs={'placeholder': _('Your email address')})
    )

class UserSettingsForm(ModelFormWithPlaceholders):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
        }

        placeholders = {
            'first_name': _('Your first name'),
            'last_name': _('Your last name'),
        }