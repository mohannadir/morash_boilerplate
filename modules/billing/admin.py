from django.utils.translation import gettext_lazy as _

from modules.billing.models import Subscription
from unfold.admin import StackedInline

class SubscriptionInline(StackedInline):
    model = Subscription
    can_delete = False
    verbose_name_plural = _('Subscription')
    fk_name = 'user'