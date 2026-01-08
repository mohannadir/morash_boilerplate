from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseUser(AbstractUser):
    
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    credits_balance = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def get_stripe_customer(self):
        from modules.payments.utils import get_or_create_stripe_customer
        return get_or_create_stripe_customer(self)
    
    def cancel_subscription(self):
        from modules.billing.utils import cancel_subscription_for_user
        return cancel_subscription_for_user(self)

    def get_subscription(self) -> dict | None:
        from modules.billing.utils import get_subscription_by_key

        if self.subscription and self.subscription.is_active():
            subscription_key = self.subscription.subscription_key
        else:
            subscription_key = 'default'

        subscription_metadata = get_subscription_by_key(subscription_key)
        subscription_dict = self.subscription.to_dict() if self.subscription else {}

        data = {
            **subscription_dict,
            **subscription_metadata,
        }
        data.update({'key' : subscription_key})

        return data

    def get_initials(self):
        return f'{self.first_name[0]}{self.last_name[0]}'.upper() if self.first_name and self.last_name else f'{self.username[0]}{self.username[1]}'.upper()

    def send_forgot_password_email(self):
        from modules.emails.utils import send_user_forgot_password_email
        send_user_forgot_password_email(self)

    def send_activation_email(self):
        from modules.emails.utils import send_user_activation_email
        send_user_activation_email(self)

    def add_credits(self, amount: int, reason: str = 'Added credits to account'):
        from modules.billing.utils import add_credits_to_user
        return add_credits_to_user(self, amount, reason)

    def consume_credits(self, amount: int, action: str):
        from modules.billing.utils import consume_credit_for_user
        return consume_credit_for_user(self, amount, action)

    def has_credits(self, amount: int) -> bool:
        return self.credits_balance >= amount