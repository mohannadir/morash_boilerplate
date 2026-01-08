import stripe
from django.conf import settings
from django.contrib.auth import get_user_model

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_or_create_stripe_customer(user: get_user_model) -> stripe.Customer:
    """ Tries to retrieve the stripe customer for the user. If it doesn't exist, creates it. """

    if not user.stripe_customer_id:
        stripe_customer = stripe.Customer.create(
            email=user.email,
            name=user.get_full_name(),
            description=f"Stripe customer for {user.get_full_name()}",
            metadata={
                'user_id': user.id
            }
        )

        user.stripe_customer_id = stripe_customer.id
        user.save()
    
    # try to return the customer by our saved id
    # if Stripe can't find it, create it again
    try:
        customer = stripe.Customer.retrieve(user.stripe_customer_id)

        # Deleted customers are still present in Stripe
        # but they have a deleted attribute set to True
        # If that's the case, we need to create a new customer
        if getattr(customer, 'deleted', False):
            user.stripe_customer_id = None
            user.save()
            return get_or_create_stripe_customer(user)
        return customer
    except stripe.error.InvalidRequestError as e:
        user.stripe_customer_id = None
        user.save()
        return get_or_create_stripe_customer(user)

def get_user_by_stripe_customer_id(stripe_customer_id: str) -> get_user_model:
    """ Retrieves the user by the stripe customer id. """

    return get_user_model().objects.filter(stripe_customer_id=stripe_customer_id).first()

def get_line_items_for_checkout(checkout_session_id: str) -> list[dict]:
    """ Retrieves the line items for a checkout session. """

    session = stripe.checkout.Session.list_line_items(checkout_session_id)
    return session.data

def create_stripe_invoice_for_price_for_user(user: get_user_model, price_id: str, mark_paid: bool = False) -> stripe.Invoice:
    """ Creates a stripe invoice for the user. 

        :param user: The user to create the invoice for.
        :param price_id: The price id to create the invoice for.
        :param mark_paid: Whether to mark the invoice as paid.
        :return: The created invoice.
    """

    if not user.stripe_customer_id:
        return None

    invoice = stripe.Invoice.create(
        customer=user.stripe_customer_id
    )

    stripe.InvoiceItem.create(
        customer=user.stripe_customer_id,
        price=price_id,
        invoice=invoice.id
    )

    stripe.Invoice.finalize_invoice(invoice.id)
    if mark_paid:
        stripe.Invoice.pay(invoice.id, paid_out_of_band=True)

    return invoice