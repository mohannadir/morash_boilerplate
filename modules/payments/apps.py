from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.payments'

    def ready(self):
        import modules.payments.signals
        import modules.payments.webhooks