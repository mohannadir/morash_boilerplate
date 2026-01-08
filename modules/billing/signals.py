from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from modules.billing.models import Subscription


def create_subscription(sender, instance, created, **kwargs):
    if not hasattr(instance, 'subscription'):
        Subscription.objects.create(user=instance, subscription_key='default')

post_save.connect(create_subscription, sender=get_user_model())