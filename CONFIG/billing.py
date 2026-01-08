from django.utils.translation import gettext_lazy as _

# This is the payment model that the application will use. It can be 'subscriptions', 'credits', 'both' (subscriptions and credits), or 'none' (no billing).
# If it is 'subscriptions', the application will use the subscription model. You will need to define the subscription plans in the SUBSCRIPTIONS list below.
# If it is 'credits', the application will use the credits model. You will need to define the credit packages in the CREDIT_PACKAGES list below.
# If it is 'both', the application will use both the subscription and credits models. You will need to define the subscription plans in the SUBSCRIPTIONS list below and the credit packages in the CREDIT_PACKAGES list below.
# If it is 'none', the application will not use any billing model. You can use this option if you want to provide the service for free.

BILLING_MODEL = "subscriptions"

# The list of subscription plans that the application will use. This list is only used if BILLING_MODEL is set to 'subscriptions' or 'both'.
# Each subscription plan is a dictionary with the following keys
# - key: A unique key for the subscription plan. This key is used to identify the subscription plan in the code.
# - name: The name of the subscription plan.
# - icon: The name of the icon to use for the subscription plan. This should be the name of a Feather icon.
# - description: A description of the subscription plan.
# - price: A dictionary with the following keys
#   - value: The price of the subscription plan.
#   - currency_symbol: The currency symbol of the price.
# - stripe_price_id: The ID of the Stripe price object for the subscription plan. This is used to create the subscription in Stripe.
# - show: Whether to show the subscription plan on the pricing page.
# - lifetime: Whether the subscription plan is a lifetime subscription.
# - included: A list of features included in the subscription plan. This is shown on the billing page and the landing page, if available.
# - not_included: A list of features not included in the subscription plan. This is shown on the billing page and the landing page, if available.
# For lifetime subscriptions, you need to make a "one-time" price in Stripe and add the price ID here. For monthly subscriptions, you need to make a "recurring" price in Stripe and add the price ID here.
# For free subscriptions, you need to set the price to 0.00. The stripe_price_id is not required for free subscriptions. You can set the show key to False to hide the free subscription plan from the pricing page.

SUBSCRIPTIONS = [
    {
        'key' : 'default',
        'name' : _('Free tier'),
        'icon' : 'smile',
        'description' : _('For those who want to try out the service before committing'),
        'price' : {
            'value' : 0.00,
            'currency_symbol' : '€',
        },
        'show' : False,
    },
    {
        'key' : 'lifetime',
        'name' : _('Lifetime license'),
        'description' : _('Enjoy all the features of the service forever'),
        'icon' : 'thumbs-up',
        'price' : {
            'value' : 299.00,
            'currency_symbol' : '€',
        },
        'stripe_price_id' : 'price_1PKewlRq8MH1iNLlqTtsRHrL',
        'show' : True,
        'lifetime' : True,
        'included': [_('One good thing'), _('One other good thing'), _('And one more good thing')],
        'not_included': [_('One bad thing'), _('One other bad thing'), _('And one more bad thing')],
    },
    {
        'key' : 'monthly',
        'name' : _('Monthly subscription'),
        'description' : _('Enjoy all the features of the service for a month'),
        'icon' : 'calendar',
        'price' : {
            'value' : 20.00,
            'currency_symbol' : '€',
        },
        'stripe_price_id' : 'price_1PKexCRq8MH1iNLl6Bub67Op',
        'show' : True,
        'lifetime' : False,
        'included': [_('One good thing'), _('One other good thing'), _('And one more good thing')],
        'not_included': [_('One bad thing'), _('One other bad thing'), _('And one more bad thing')],
    }
]

# The list of credit packages that the application will use. This list is only used if BILLING_MODEL is set to 'credits' or 'both'.
# Each credit package is a dictionary with the following keys
# - key: A unique key for the credit package. This key is used to identify the credit package in the code.
# - name: The name of the credit package.
# - icon: The name of the icon to use for the credit package. This should be the name of a Feather icon.
# - description: A description of the credit package.
# - price: A dictionary with the following
#   - value: The price of the credit package.
#   - currency_symbol: The currency symbol of the price.
# - stripe_price_id: The ID of the Stripe price object for the credit package. This is used to create the checkout session in Stripe.
# - show: Whether to show the credit package on the pricing page.
# - credits: The number of credits in the credit package.

CREDIT_PACKAGES = [
    {
        'key' : 'ten_credits',
        'name' : _('10 credits'),
        'description' : _('Get 10 credits to use on the service'),
        'icon' : 'thumbs-up',
        'price' : {
            'value' : 10.00,
            'currency_symbol' : '€',
        },
        'stripe_price_id' : 'price_1PNE60Rq8MH1iNLlO6gf9B55',
        'show' : True,
        'credits' : 10,
    },
    {
        'key' : 'twenty_five_credits',
        'name' : _('25 credits'),
        'description' : _('Get 25 credits to use on the service'),
        'icon' : 'heart',
        'price' : {
            'value' : 22.50,
            'currency_symbol' : '€',
        },
        'stripe_price_id' : 'price_1PNE6KRq8MH1iNLl1708k33a',
        'show' : True,
        'credits' : 25,
    },
    {
        'key' : 'fifty_credits',
        'name' : _('50 credits'),
        'description' : _('Get 50 credits to use on the service'),
        'icon' : 'star',
        'price' : {
            'value' : 43.00,
            'currency_symbol' : '€',
        },
        'stripe_price_id' : 'price_1PNEFTRq8MH1iNLlTH6ivdZN',
        'show' : True,
        'credits' : 50,
    },
]