from django.contrib.auth import get_user_model
from rest_framework import serializers

from modules.billing.models import Subscription, StripeInvoice, CreditAction

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        exclude = ['id', 'user']

class StripeInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeInvoice
        exclude = ['id', 'user']

class CreditActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAction
        exclude = ['id', 'user']

class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'date_joined' , 'stripe_customer_id', 'credits_balance', 'subscription']