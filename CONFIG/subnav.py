from django.utils.translation import gettext_lazy as _
from django.conf import settings

GLOBAL_SUBNAV = [
    {
        'key' : 'default',
        'name' : _('Default'),
        'show_title' : False,
        'is_active' : True,
        'items' : [{
            'key': 'dashboard',
            'name': _('Dashboard'),
            'url_name' : 'main:dashboard',
            'icon': 'circle',
            'is_active': True,
        },
        {
            'key': 'adminpanel',
            'name': _('Adminpanel'),
            'url_name' : 'admin:index',
            'icon': 'hexagon',
            'is_active': True,
            'superuser_required': True,
        },
        ]
    },
    {
        'key' : 'account_settings',
        'name' : _('Account settings'),
        'show_title' : True,
        'is_active' : True,
        'items' : [{
            'key': 'billing',
            'name': _('Billing'),
            'url_name' : 'billing:manage_billing',
            'icon': 'credit-card',
            'is_active': True,
        },
        {
            'key': 'settings',
            'name': _('Settings'),
            'url_name' : 'authentication:user_settings',
            'icon': 'settings',
            'is_active': True,
        },
        {
            'key': 'logout',
            'name': _('Logout'),
            'url_name' : 'authentication:logout',
            'icon': 'log-out',
            'is_active': True,
        }]
    }
]

# If the shipwithdjang.examples app is enabled, add the examples subnav to the global subnav
if 'modules.examples' in settings.INSTALLED_APPS:
    try:
        from modules.examples.subnav import EXAMPLES_SUBNAV
        GLOBAL_SUBNAV.insert(1, EXAMPLES_SUBNAV)
    except ImportError:
        pass