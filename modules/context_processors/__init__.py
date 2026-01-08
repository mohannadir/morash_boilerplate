from modules.utils.subnav import get_visible_subnav_for_user

from django.conf import settings
from CONFIG.authentication import ALLOW_GITHUB_LOGIN, ALLOW_LINKED_IN_LOGIN, ALLOW_THIRD_PARTY_LOGIN, ALLOW_REGISTRATIONS

def add_global_subnav(request):
    return {
        'GLOBAL_SUBNAV': get_visible_subnav_for_user(request.user)
    }

def add_platform_config(request):
    return {
        'PLATFORM_NAME' : settings.PLATFORM_NAME,
        'PLATFORM_TAGLINE': settings.PLATFORM_TAGLINE,
        'PLATFORM_VERSION' : settings.PLATFORM_VERSION,
        'BILLING_MODEL' : settings.BILLING_MODEL
    }
