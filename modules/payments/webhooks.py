from .webhook_handler import receive
from django.contrib.auth import get_user_model
from modules.billing.utils import get_subscription_by_price_id, get_credit_package_by_price_id
from modules.payments.utils import get_user_by_stripe_customer_id, get_line_items_for_checkout, create_stripe_invoice_for_price_for_user

from modules.billing.models import StripeInvoice

from django.utils.translation import gettext_lazy as _

@receive('customer.deleted')
def delete_customer(event, **kwargs):
    customer_data = event['data']['object']
    user = get_user_model().objects.filter(stripe_customer_id=customer_data['id']).first()
    if user:
        user.stripe_customer_id = None
        user.save()

@receive('invoice.paid')
def paid_invoice(event, **kwargs):
    invoice_data = event['data']['object']
    user = get_user_model().objects.filter(stripe_customer_id=invoice_data['customer']).first()
    if user and not user.subscription.lifetime:
        user.subscription.current_period_start = invoice_data['lines']['data'][0]['period']['start']
        user.subscription.current_period_end = invoice_data['lines']['data'][0]['period']['end']
        user.subscription.save()

@receive('customer.subscription.created')
@receive('customer.subscription.updated')
def create_or_update_subscription(event, **kwargs):
    subscription_data = event['data']['object']
    try:
        subscription = get_subscription_by_price_id(subscription_data['items']['data'][0]['price']['id'])
    except:
        return
    
    if not subscription:
        return

    user = get_user_model().objects.filter(stripe_customer_id=subscription_data['customer']).first()
    if user:
        user.subscription.stripe_subscription_id = subscription_data['id']
        user.subscription.stripe_status = subscription_data['status']

        user.subscription.subscription_key = subscription['key']
        user.subscription.starts = subscription_data['start_date']
        user.subscription.current_period_start = subscription_data['current_period_start']
        user.subscription.current_period_end = subscription_data['current_period_end']
        user.subscription.cancel_at_period_end = subscription_data['cancel_at_period_end']
        user.subscription.lifetime = False # Stripe subscriptions are never lifetime

        user.subscription.save()

@receive('customer.subscription.deleted')
def delete_subscription(event, **kwargs):
    subscription_data = event['data']['object']
    user = get_user_model().objects.filter(stripe_customer_id=subscription_data['customer']).first()
    if user:
        user.subscription.reset_to_default()

@receive('invoice.finalized')
def add_invoice(event, **kwargs):
    invoice_data = event['data']['object']
    user = get_user_by_stripe_customer_id(invoice_data['customer'])
    if user:
        StripeInvoice.objects.create(
            user=user,
            stripe_id=invoice_data['id'],
            number=invoice_data['number'],
            hosted_invoice_url=invoice_data['hosted_invoice_url']
        )

@receive('checkout.session.completed')
def create_onetime_subscription(event, **kwargs):
    session_data = event['data']['object']
    user = get_user_by_stripe_customer_id(session_data['customer'])

    line_items = get_line_items_for_checkout(session_data['id'])
    if len(line_items) == 0 or 'price' not in line_items[0]:
        return
    
    subscription = get_subscription_by_price_id(line_items[0]['price']['id'])
    if not subscription or not subscription.get('lifetime', False):
        return

    if user:

        # Set the new subscriptipn
        user.subscription.stripe_subscription_id = None
        user.subscription.stripe_status = 'active'

        user.subscription.subscription_key = subscription['key']
        user.subscription.lifetime = True
        user.subscription.starts = session_data['created']
        user.subscription.current_period_start = session_data['created']
        user.subscription.current_period_end = 4102441200 # 2100-01-01, really far in the future. By then, we're all dead (or bankrupt)
        user.subscription.cancel_at_period_end = False

        user.subscription.save()

        # Request Stripe to create an invoice (this is not done automatically for one-time payments)
        create_stripe_invoice_for_price_for_user(user, line_items[0]['price']['id'], mark_paid=True)

@receive('checkout.session.completed')
def add_credits_to_user(event, **kwargs):
    session_data = event['data']['object']
    user = get_user_by_stripe_customer_id(session_data['customer'])

    line_items = get_line_items_for_checkout(session_data['id'])
    if len(line_items) == 0 or 'price' not in line_items[0]:
        return
    
    credit_package = get_credit_package_by_price_id(line_items[0]['price']['id'])
    if not credit_package:
        return

    if user:
        user.add_credits(credit_package['credits'], _(f'Bought {credit_package["credits"]} credits for {credit_package["price"]["currency_symbol"]} {credit_package["price"]["value"]} '))
        user.save()

        # Request Stripe to create an invoice (this is not done automatically for one-time payments)
        create_stripe_invoice_for_price_for_user(user, line_items[0]['price']['id'], mark_paid=True)