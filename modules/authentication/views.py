from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView
from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from modules.authentication.tokens import account_activation_token

from allauth.mfa.models import Authenticator

from .forms import UserRegisterForm, UserLoginForm, UserForgotPasswordForm, UserSettingsForm

from django.contrib.auth import get_user_model

class UserLogin(auth_views.LoginView):
    """ This view allows users to log in. """

    form_class = UserLoginForm
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ALLOW_REGISTRATIONS'] = settings.ALLOW_REGISTRATIONS
        context['ALLOW_THIRD_PARTY_LOGIN'] = settings.ALLOW_THIRD_PARTY_LOGIN
        context['ALLOW_GITHUB_LOGIN'] = settings.ALLOW_GITHUB_LOGIN
        context['ALLOW_LINKED_IN_LOGIN'] = settings.ALLOW_LINKED_IN_LOGIN
        return context

    def get_success_url(self):
        return reverse(settings.LOGIN_REDIRECT_URL)
    
class UserLogout(LoginRequiredMixin, View):
    """ This view allows users to log out. """
        
    def get(self, request):
        logout(request)
        messages.success(request, _("You've been logged out."))
        return redirect(settings.LOGOUT_REDIRECT_URL)
    
class UserRegister(CreateView):
    """ This view allows users to register. """
    
    model = get_user_model()
    form_class = UserRegisterForm
    template_name = 'authentication/signup.html'
    
    def get_success_url(self):
        messages.success(self.request, _("We've created your account! Check your email to verify your account."))
        return reverse(settings.LOGIN_URL)
    
    def dispatch(self, request, *args, **kwargs):
        if not settings.ALLOW_REGISTRATIONS:
            messages.error(request, _("Registrations are disabled."))
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)
    
class UserSettings(LoginRequiredMixin, UpdateView):
    """ This view allows users to update their settings. """
    
    model = get_user_model()
    form_class = UserSettingsForm
    template_name = 'authentication/settings.html'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['totp_authenticator'] = Authenticator.objects.filter(user=self.request.user, type=Authenticator.Type.TOTP).first()
        return context
    
    def get_success_url(self):
        messages.success(self.request, _("Your settings have been updated."))
        return reverse('authentication:user_settings')
    
class UserActivate(View):
    """ This view allows users to activate their accounts. """

    def get(self, request, *args, **kwargs):

        try:
            uid = force_str(urlsafe_base64_decode(kwargs['uidb64']))
            user = get_user_model().objects.get(pk=uid)
        except Exception as e:
            user = None
        
        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, _('Welcome! Your account has been activated.'))
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, _('Invalid activation link.'))
            return redirect(settings.LOGIN_URL)
        
class UserForgotPassword(FormView):
    """ This view allows users to reset their passwords. 
        This view is used to send the user an email with instructions on how to reset their password.
    """
    
    template_name = 'authentication/forgot_password.html'
    form_class = UserForgotPasswordForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email', None)
        user = get_user_model().objects.filter(username=email).first()
        if user is not None:
            user.send_forgot_password_email()
        return super().form_valid(form)
   
    def get_success_url(self):
        messages.success(self.request, _("We've sent you an email with instructions on how to reset your password."))
        return reverse(settings.LOGIN_URL)

class UserResetPassword(auth_views.PasswordResetConfirmView):
    """ This view is used to reset the user's password. The user sets a new password. """
    
    template_name = 'authentication/reset_password.html'
    
    def get_success_url(self):
        messages.success(self.request, _("Your password has been reset."))
        return reverse(settings.LOGIN_URL)
    
class UserChangePassword(auth_views.PasswordChangeView):
    """ This view allows users to change their password. """
    
    template_name = 'authentication/change_password.html'
    
    def get_success_url(self):
        messages.success(self.request, _("Your password has been changed."))
        return reverse('authentication:user_settings')