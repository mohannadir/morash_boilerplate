from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect

class UserHasSubscriptionMixin:
    required_subscription = None
    
    def get_required_subscription(self):
        if self.required_subscription is None:
            raise ValueError("required_subscription is not set. Please set the required_subscription attribute or override the get_required_subscription method.")
        
        if isinstance(self.required_subscription, str):
            return [self.required_subscription]
        
        if not isinstance(self.required_subscription, list):
            raise ValueError("required_subscription must be a string or a list of strings.")
        
        return self.required_subscription

    def dispatch(self, request, *args, **kwargs):

        # User is not logged in
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        
        # User doesn't have a valid subscription
        if not hasattr(request.user, 'subscription'):
            raise PermissionDenied()
        
        # User doesn't have the required permission
        if not request.user.subscription.subscription_key in self.get_required_subscription():
            raise PermissionDenied()
        
        return super().dispatch(request, *args, **kwargs)
    
class CreditActionMixin:
    amount_of_credits = None
    action = None
    consume_credits_on = None # 'GET' or 'POST'
    
    def get_amount_of_credits(self):
        if self.amount_of_credits is None:
            raise ValueError("amount_of_credits is not set. Please set the amount_of_credits attribute or override the get_amount_of_credits method.")
        
        return self.amount_of_credits
    
    def get_action(self):
        if self.action is None:
            raise ValueError("action is not set. Please set the action attribute or override the get_action method.")
        
        return self.action
    
    def get_consume_credits_on(self):
        if self.consume_credits_on is None:
            raise ValueError("consume_credits_on is not set. Please set the consume_credits_on attribute or override the get_consume_credits_on method.")
        
        if self.consume_credits_on.lower() not in ['get', 'post']:
            raise ValueError("consume_credits_on must be either 'GET' or 'POST'.")
        
        return self.consume_credits_on.lower()
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) if hasattr(super(), 'get') else HttpResponseRedirect(self.get_success_url())
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs) if hasattr(super(), 'post') else HttpResponseRedirect(self.get_success_url())
    
    def get_failed_url(self):
        raise NotImplementedError("Please implement the get_failed_url method.")
    
    def get_success_url(self):
        raise NotImplementedError("Please implement the get_success_url method.")
    
    def dispatch(self, request, *args, **kwargs):
        # User is not logged in
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        
        if self.get_consume_credits_on() == request.method.lower():
            if request.user.credits_balance < self.get_amount_of_credits():
                return redirect(self.get_failed_url())
            
            request.user.consume_credits(self.get_amount_of_credits(), self.get_action())
        
        return super().dispatch(request, *args, **kwargs)