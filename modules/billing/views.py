from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from modules.views import DynamicTableData
import modules.billing.utils as billing
from modules.billing.models import StripeInvoice, CreditAction


class InvoiceTableData(LoginRequiredMixin, DynamicTableData):
    template_name = 'billing/invoices/tables/data.html'
    model = StripeInvoice
    context_object_name = 'invoices'
    sort_options = [{ 'name': 'Number', 'field': 'number', }, { 'name': 'Date', 'field': 'created_at', }]
    sort_default = '-created_at'
    search_fields = ['number']

    def get_queryset(self):
        return self.request.user.invoices.all()
    
class CreditActionsTableData(LoginRequiredMixin, DynamicTableData):
    template_name = 'billing/credits/tables/data.html'
    model = CreditAction
    context_object_name = 'credit_actions'
    sort_options = [{ 'name': 'Date', 'field': 'created_at', }, { 'name': 'Amount', 'field': 'amount', }]
    sort_default = '-created_at'
    search_fields = ['action', 'amount']

    def get_queryset(self):
        return self.request.user.credit_actions.all()

class ManageBilling(LoginRequiredMixin, TemplateView):
    ''' Billing management page for users. '''

    template_name = 'billing/manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billing_model'] = settings.BILLING_MODEL
        context['subscriptions'] = billing.SUBSCRIPTIONS
        context['credit_packages'] = billing.CREDIT_PACKAGES
        return context

class SubscripeToSubscription(LoginRequiredMixin, View):
    ''' Subscribe user to a subscription.
    
        This view is called when user clicks on the subscribe button.
    '''

    def get(self, request, *args, **kwargs):
        price_id = self.subscription_data.get('stripe_price_id')
        return redirect(reverse('payments:setup_checkout_for_price', kwargs={'price_id': price_id}))

    def dispatch(self, request, *args, **kwargs):
        subscription_key = self.kwargs.get('subscription_key')

        self.subscription_data = billing.get_subscription_by_key(subscription_key)
        if not self.subscription_data or not self.subscription_data.get('stripe_price_id'):
            messages.error(request, _('Invalid subscription key'))
            return redirect('billing:manage_billing')
        
        if subscription_key not in billing.VALID_SUBSCRIPTION_KEYS:
            messages.error(request, _('Invalid subscription key'))
            return redirect('billing:manage_billing')
        
        if subscription_key == request.user.get_subscription()['key']:
            messages.info(request, _('You are already subscribed to this subscription'))
            return redirect('billing:manage_billing')

        return super().dispatch(request, *args, **kwargs)
    
class CancelSubscription(LoginRequiredMixin, View):
    ''' Cancel user's subscription.
    
        This view is called when user clicks on the cancel subscription button.
    '''

    template_name = 'billing/subscriptions/cancel_subscription.html'

    def get(self, request, *args, **kwargs):
        context = {
            'subscription': request.user.get_subscription(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        subscription_cancelled = request.user.cancel_subscription()
        if subscription_cancelled:
            messages.info(request, _("You've successfully cancelled your subscription. You will not be charged again."))
        else:
            messages.error(request, _("Failed to cancel subscription. Please try again. If the problem persists, contact support."))

        return redirect('billing:manage_billing')
    
class PurchaseCreditsPackage(LoginRequiredMixin, View):
    ''' Purchase credits package.
    
        This view is called when user clicks on the purchase credits button.
    '''

    def get(self, request, *args, **kwargs):
        price_id = self.credit_package_data.get('stripe_price_id')
        return redirect(reverse('payments:setup_checkout_for_price', kwargs={'price_id': price_id}))

    def dispatch(self, request, *args, **kwargs):
        credit_package_key = self.kwargs.get('credit_package_key')

        self.credit_package_data = billing.get_credit_package_by_key(credit_package_key)
        if not self.credit_package_data:
            messages.error(request, _('Invalid price ID'))
            return redirect('billing:manage_billing')
        
        return super().dispatch(request, *args, **kwargs)