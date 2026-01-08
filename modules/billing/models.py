from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Subscription(models.Model):

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='subscription')
    subscription_key = models.CharField(max_length=255)

    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_status = models.CharField(max_length=255, blank=True, null=True)

    starts = models.BigIntegerField(default=0) # Unix timestamp
    current_period_start = models.BigIntegerField(default=0) # Unix timestamp
    current_period_end = models.BigIntegerField(default=0) # Unix timestamp

    cancel_at_period_end = models.BooleanField(default=False)
    lifetime = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - Subscription: {self.subscription_key}"
    
    def to_dict(self):
        fields = [field.name for field in self._meta.get_fields() if field.name != 'user'] # remove the user field, as it's a ForeignKey
        methods = ['is_default', 'can_be_cancelled', 'marked_for_cancellation', 'cancels_at', 'renews_at', 'is_active']

        result = {}
        for field in fields:
            if callable(field):
                result[field] = getattr(self, field)()
            else:
                result[field] = getattr(self, field)

        for method in methods:
            result[method] = getattr(self, method)()
        
        return result
    
    def is_default(self):
        return self.subscription_key == 'default'
    
    def reset_to_default(self):
        self.subscription_key = 'default'
        self.stripe_subscription_id = None
        self.stripe_status = None
        self.starts = 0
        self.current_period_start = 0
        self.current_period_end = 0
        self.cancel_at_period_end = False
        self.save()

    def can_be_cancelled(self):
        return self.stripe_subscription_id is not None and not self.is_default() and not self.lifetime and not self.marked_for_cancellation()

    def marked_for_cancellation(self):
        return self.cancel_at_period_end and not self.lifetime and not self.is_default()
    
    def cancels_at(self):
        if self.cancel_at_period_end:
            return timezone.datetime.fromtimestamp(self.current_period_end)
        return None

    def renews_at(self):
        if self.current_period_end == 0:
            return None
        return timezone.datetime.fromtimestamp(self.current_period_end)
    
    def is_active(self):
        return self.current_period_end > timezone.now().timestamp() and self.stripe_status == 'active'
    
class StripeInvoice(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='invoices')
    stripe_id = models.CharField(max_length=255)

    number = models.CharField(max_length=255)
    hosted_invoice_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.number}'
    
class CreditAction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='credit_actions')
    amount = models.IntegerField()
    action = models.CharField(max_length=255)

    credits_before = models.IntegerField()
    credits_after = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.action}'