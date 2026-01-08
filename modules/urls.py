from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('authentication/', include(('modules.authentication.urls', 'authentication'), namespace='authentication')),
    path('billing/', include(('modules.billing.urls', 'billing'), namespace='billing')),
    path('payments/', include(('modules.payments.urls', 'payments'), namespace='payments')),
    path('utils/', include(('modules.utils.urls', 'utils'), namespace='utils')),

    path('examples/', include(('modules.examples.urls', 'examples'), namespace='examples')),

    # Redirect the 2FA index to the user settings page
    path('accounts/2fa/', RedirectView.as_view(pattern_name='authentication:user_settings')),

    # Third-party apps
    path('accounts/', include('allauth.urls')),
    path('impersonate/', include('impersonate.urls')),
]