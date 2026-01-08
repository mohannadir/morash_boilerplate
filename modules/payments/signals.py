from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .utils import get_or_create_stripe_customer

def create_stripe_customer_for_user(sender, instance, created, **kwargs):
    if created:
        get_or_create_stripe_customer(instance)

post_save.connect(create_stripe_customer_for_user, sender=get_user_model())