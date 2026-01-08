# Power on self test
# Path: base/base/urls.py

from CONFIG.billing import SUBSCRIPTIONS, BILLING_MODEL, CREDIT_PACKAGES
from CONFIG.emails import EMAIL_PROVIDER, SENDGRID_API_KEY
from CONFIG.secrets import SECRETS_MANAGER, INFISICAL_PROJECT_ID, INFISICAL_CLIENT_ID, INFISICAL_CLIENT_SECRET, INFISICAL_ENVIRONMENT, AWS_SECRET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, AZURE_KEY_VAULT_NAME

class PowerOnSelfTest:
    def __init__(self):
        self.ran_tests = []
        self.failed_tests = {}
        self.passed_tests = []
        self.skipped_tests = []

        self.run()

    def run(self):
        self.test_billing()
        self.test_emails()
        self.test_secrets()

        self.raise_fail_or_pass()

    def test_billing(self):
        billing_errors = []
        default_subscription = None

        ## Check BILLING_MODEL
        if BILLING_MODEL not in ['subscriptions', 'credits', 'both', 'none']:
            billing_errors.append(f'Invalid value for BILLING_MODEL: {BILLING_MODEL}. The value of BILLING_MODEL should be "subscriptions", "credits" or "both".')

        ## If BILLING_MODEL is 'subscriptions' or 'both', check that SUBSCRIPTIONS is not empty
        if BILLING_MODEL in ['subscriptions', 'both']:
            if len(SUBSCRIPTIONS) == 0:
                billing_errors.append('No subscription plans found. Please add at least one subscription plan to the SUBSCRIPTIONS list in CONFIG/subscriptions.py.')

            # Check that each subscription has the required keys
            for subscription in SUBSCRIPTIONS:
                required_keys = ['key', 'name', 'description', 'icon', 'price', 'show']
                for key in required_keys:
                    if key not in subscription:
                        billing_errors.append(f'Subscription with key "{subscription["key"]}" is missing the key "{key}".')

                if 'price' in subscription:
                    if 'value' not in subscription['price']:
                        billing_errors.append(f'Subscription with key "{subscription["key"]}" is missing the key "value" in the price dictionary.')
                    if 'currency_symbol' not in subscription['price']:
                        billing_errors.append(f'Subscription with key "{subscription["key"]}" is missing the key "currency_symbol" in the price dictionary.')

                if subscription['key'] == 'default':
                    default_subscription = subscription
            
            if default_subscription is None:
                billing_errors.append('No subscription with key "default" found. Please add a subscription with the key "default" to the SUBSCRIPTIONS list in CONFIG/subscriptions.py.')
        
        # If BILLING_MODEL is 'credits' or 'both', check that CREDIT_PACKAGES is not empty
        if BILLING_MODEL in ['credits', 'both']:
            if len(CREDIT_PACKAGES) == 0:
                billing_errors.append('No credit packages found. Please add at least one credit package to the CREDIT_PACKAGES list in CONFIG/subscriptions.py.')

            # Check that each credit package has the required keys
            for credit_package in CREDIT_PACKAGES:
                required_keys = ['key', 'name', 'description', 'price']
                for key in required_keys:
                    if key not in credit_package:
                        billing_errors.append(f'Credit package with key "{credit_package["key"]}" is missing the key "{key}".')
                
                if 'price' in credit_package:
                    if 'value' not in credit_package['price']:
                        billing_errors.append(f'Credit package with key "{credit_package["key"]}" is missing the key "value" in the price dictionary.')
                    if 'currency_symbol' not in credit_package['price']:
                        billing_errors.append(f'Credit package with key "{credit_package["key"]}" is missing the key "currency_symbol" in the price dictionary.')


        self.ran_tests.append('test_billing')
        if len(billing_errors) > 0:
            self.failed_tests['test_billing'] = billing_errors
        else:
            self.passed_tests.append('test_billing')

    def test_emails(self):
        email_errors = []

        if EMAIL_PROVIDER == 'sendgrid':
            if SENDGRID_API_KEY is None or SENDGRID_API_KEY == '':
                email_errors.append("You're using SendGrid as the email provider but SENDGRID_API_KEY is not set. Please set the SENDGRID_API_KEY in the CONFIG/emails.py file.")
        elif EMAIL_PROVIDER != 'smtp':
            email_errors.append(f'Invalid value for EMAIL_PROVIDER: {EMAIL_PROVIDER}. The value of EMAIL_PROVIDER should be "smtp" or "sendgrid".')

        self.ran_tests.append('test_emails')
        if len(email_errors) > 0:
            self.failed_tests['test_emails'] = email_errors
        else:
            self.passed_tests.append('test_emails')

    def test_secrets(self):
        errors = []

        if SECRETS_MANAGER not in ['infisical', 'aws', 'azure', 'env']:
            errors.append(f'Invalid value for SECRETS_MANAGER: {SECRETS_MANAGER}. The value of SECRETS_MANAGER should be "infisical", "aws", "azure" or "env".')

        if SECRETS_MANAGER == 'infisical':
            if INFISICAL_PROJECT_ID is None or INFISICAL_PROJECT_ID == '':
                errors.append('INFISICAL_PROJECT_ID is not set. Please set the INFISICAL_PROJECT_ID in the CONFIG/secrets.py file.')
            if INFISICAL_CLIENT_ID is None or INFISICAL_CLIENT_ID == '':
                errors.append('INFISICAL_CLIENT_ID is not set. Please set the INFISICAL_CLIENT_ID in the CONFIG/secrets.py file.')
            if INFISICAL_CLIENT_SECRET is None or INFISICAL_CLIENT_SECRET == '':
                errors.append('INFISICAL_CLIENT_SECRET is not set. Please set the INFISICAL_CLIENT_SECRET in the CONFIG/secrets.py file.')
            if INFISICAL_ENVIRONMENT is None or INFISICAL_ENVIRONMENT == '':
                errors.append('INFISICAL_ENVIRONMENT is not set. Please set the INFISICAL_ENVIRONMENT in the CONFIG/secrets.py file.')

        if SECRETS_MANAGER == 'aws':
            if AWS_SECRET_NAME is None or AWS_SECRET_NAME == '':
                errors.append('AWS_SECRET_NAME is not set. Please set the AWS_SECRET_NAME in the CONFIG/secrets.py file.')
            if AWS_ACCESS_KEY_ID is None or AWS_ACCESS_KEY_ID == '':
                errors.append('AWS_ACCESS_KEY_ID is not set. Please set the AWS_ACCESS_KEY_ID in the CONFIG/secrets.py file.')
            if AWS_SECRET_ACCESS_KEY is None or AWS_SECRET_ACCESS_KEY == '':
                errors.append('AWS_SECRET_ACCESS_KEY is not set. Please set the AWS_SECRET_ACCESS_KEY in the CONFIG/secrets.py file.')
            if AWS_REGION is None or AWS_REGION == '':
                errors.append('AWS_REGION is not set. Please set the AWS_REGION in the CONFIG/secrets.py file.')

        if SECRETS_MANAGER == 'azure':
            if AZURE_CLIENT_ID is None or AZURE_CLIENT_ID == '':
                errors.append('AZURE_CLIENT_ID is not set. Please set the AZURE_CLIENT_ID in the CONFIG/secrets.py file.')
            if AZURE_TENANT_ID is None or AZURE_TENANT_ID == '':
                errors.append('AZURE_TENANT_ID is not set. Please set the AZURE_TENANT_ID in the CONFIG/secrets.py file.')
            if AZURE_CLIENT_SECRET is None or AZURE_CLIENT_SECRET == '':
                errors.append('AZURE_CLIENT_SECRET is not set. Please set the AZURE_CLIENT_SECRET in the CONFIG/secrets.py file.')
            if AZURE_KEY_VAULT_NAME is None or AZURE_KEY_VAULT_NAME == '':
                errors.append('AZURE_KEY_VAULT_NAME is not set. Please set the AZURE_KEY_VAULT_NAME in the CONFIG/secrets.py file.')

        self.ran_tests.append('test_secrets')
        if len(errors) > 0:
            self.failed_tests['test_secrets'] = errors
        else:
            self.passed_tests.append('test_secrets')

    def raise_fail_or_pass(self):
        if len(self.failed_tests) > 0:
            output = f'''Power on self test failed.\nFailed tests: {", ".join(list(self.failed_tests.keys()))}\n\n'''
            
            for test, errors in self.failed_tests.items():
                output += f'{test} failed with the following errors:\n'
                for error in errors:
                    output += f'- ERROR: {error}\n'
                output += '\n\n'
            
            output += 'Please fix the errors and restart the server.'
            raise Exception(output)
        else:
            print('(ShipWithDjango) Power on self test passed.')


PowerOnSelfTest()