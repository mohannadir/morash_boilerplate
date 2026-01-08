import stripe
from django.conf import settings

from CONFIG.billing import SUBSCRIPTIONS, CREDIT_PACKAGES
from .models import CreditAction

stripe.api_key = settings.STRIPE_SECRET_KEY
VALID_SUBSCRIPTION_KEYS = [subscription['key'] for subscription in SUBSCRIPTIONS]

def cancel_subscription_for_user(user) -> bool:
    """ Cancels the subscription for the user. 
        Returns True if the subscription was cancelled, False otherwise.

        :param user: The user to cancel the subscription for.
        :type user: User
        :return: Whether the subscription was cancelled.
        :rtype: bool
    """

    if user.subscription.stripe_subscription_id:
        subscription = stripe.Subscription.retrieve(user.subscription.stripe_subscription_id)
        # Cancel the subscription at the end of the period
        stripe.Subscription.modify(
            subscription.id,
            cancel_at_period_end=True
        )

        return True

    return False

def add_credits_to_user(user, amount: int, reason: str) -> None:
    """ Adds credits to the user and logs the reason.

        :param user: The user to add the credits to.
        :type user: User
        :param amount: The amount of credits to add.
        :type amount: int
        :param reason: The reason for adding the credits.
        :type reason: str
    """

    credits_before = user.credits_balance

    user.credits_balance += amount
    user.save()

    credits_after = user.credits_balance

    CreditAction.objects.create(
        user=user,
        amount=amount,
        action=reason,
        credits_before=credits_before,
        credits_after=credits_after
    )

def consume_credit_for_user(user, amount: int, action: str) -> bool:
    """ Consumes the credit for the user and logs the action.
        Returns True if the user had enough credit to consume, False otherwise.

        :param user: The user to consume the credit for.
        :type user: User
        :param amount: The amount of credit to consume.
        :type amount: int
        :param action: The action to log.
        :type action: str
        :return: Whether the user had enough credit to consume.
        :rtype: bool

    """

    if user.credits_balance >= amount:
        credits_before = user.credits_balance

        user.credits_balance -= amount
        user.save()

        credits_after = user.credits_balance

        CreditAction.objects.create(
            user=user,
            amount=amount,
            action=action,
            credits_before=credits_before,
            credits_after=credits_after
        )

        return True

    return False

def get_subscription_by_key(subscription_key: str) -> dict | None:
    """ Get subscription by key. Returns None if not found. """

    for subscription in SUBSCRIPTIONS:
        if subscription.get('key') == subscription_key:
            return subscription
    return None

def get_subscription_by_price_id(price_id: str) -> dict | None:
    """ Get subscription by price ID. Returns None if not found. """
    for subscription in SUBSCRIPTIONS:
        if subscription.get('stripe_price_id') == price_id:
            return subscription
    return None

def get_credit_package_by_key(credit_package_key: str) -> dict | None:
    """ Get credit package by key. Returns None if not found. """
    for credit_package in CREDIT_PACKAGES:
        if credit_package.get('key') == credit_package_key:
            return credit_package
    return None

def get_credit_package_by_price_id(price_id: str) -> dict | None:
    """ Get credit package by price ID. Returns None if not found. """
    for credit_package in CREDIT_PACKAGES:
        if credit_package.get('stripe_price_id') == price_id:
            return credit_package
    return None

def get_data_and_type_for_price_id(price_id: str) -> tuple[dict, str]:
    """ Get subscription or credit package by price ID. 
        Returns (data, type) where type is either 'subscription' or 'credit_package'. Data is the subscription or credit package.
    """

    subscription = get_subscription_by_price_id(price_id)
    if subscription:
        return subscription, 'subscription'
    
    credit_package = get_credit_package_by_price_id(price_id)
    if credit_package:
        return credit_package, 'credit_package'
    
    return None, None