from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from modules.billing.utils import get_subscription_by_price_id, get_data_and_type_for_price_id
from .webhook_handler import handle_event

import stripe

class SetupCheckoutForPrice(LoginRequiredMixin, View):
    ''' Setup checkout for a given price id. '''

    def get(self, request, *args, **kwargs):

        stripe_customer = request.user.get_stripe_customer()

        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': self.price_id,
                'quantity': 1,
            }],
            mode=self.mode,
            success_url=f'{settings.PLATFORM_URL}{reverse("payments:checkout_complete")}?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{settings.PLATFORM_URL}{reverse("payments:checkout_cancelled")}',
            customer=stripe_customer.id,
            api_key=settings.STRIPE_SECRET_KEY
        )

        return redirect(checkout_session.url)

    def dispatch(self, request, *args, **kwargs):
        self.price_id = self.kwargs.get('price_id')
        data, type = get_data_and_type_for_price_id(self.price_id)

        if not self.price_id or not data or type not in ['credit_package', 'subscription']:
            messages.error(request, _("Looks like you're trying to purchase or subscribe to something that doesn't exist. Please try again."))
            return redirect('billing:manage_billing')
        
        if type == 'credit_package':
            self.mode = 'payment'
        elif type == 'subscription':
            self.mode = 'subscription' if not data.get('lifetime', False) else 'payment'

        return super().dispatch(request, *args, **kwargs)
    
class CheckoutComplete(LoginRequiredMixin, View):
    ''' Checkout complete page. '''

    template_name = 'payments/checkout/complete.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class CheckoutCancelled(LoginRequiredMixin, View):
    ''' Checkout cancelled page. '''

    template_name = 'payments/checkout/cancelled.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhook(View):
    """Stripe webhook endpoint."""

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse('Invalid payload', status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse('Invalid signature', status=400)

        # Handle the event
        handle_event(event)

        return HttpResponse(status=200)