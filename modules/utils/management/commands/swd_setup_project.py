from django.core.management.base import BaseCommand, CommandError
from modules.utils.config import set_config_value

class Command(BaseCommand):
    help = 'Command to setup the initial configuration of the project'

    ASK_CONFIG_FOR = [
        {
            'name' : 'Platform',
            'config_file' : 'platform',
            'config_values' : [
                { 'key' : 'PLATFORM_NAME', 'prompt' : 'Enter the name of the platform'},
                { 'key' : 'PLATFORM_TAGLINE', 'prompt' : 'Enter the tagline of the platform' },
                { 'key' : 'PLATFORM_VERSION', 'prompt' : 'Enter the version of the platform', 'default' : '1.0.0' },
                { 'key' : 'PLATFORM_URL', 'prompt' : 'Enter the URL of the platform', 'default' : 'http://127.0.0.1:8000' }
            ]
        },
        {
            'name' : 'Billing',
            'config_file' : 'billing',
            'config_values' : [
                { 'key' : 'BILLING_MODEL', 'prompt' : 'Enter the billing model', 'default' : 'subscriptions', 'allowed_values' : ['subscriptions', 'credits', 'both', 'none'] }
            ]
        },
        {
            'name' : 'Emailing',
            'config_file' : 'emails',
            'config_values' : [
                { 'key' : 'EMAIL_PROVIDER', 'prompt' : 'Enter the email provider', 'default' : 'smtp', 'allowed_values' : ['smtp', 'sendgrid'] },
                { 'key' : 'SENDGRID_API_KEY', 'prompt' : 'Enter the SendGrid API key', 'show_if' : 'EMAIL_PROVIDER', 'show_if_value' : 'sendgrid' },
                { 'key' : 'EMAIL_USE_TASK_QUEUE', 'prompt' : 'Use task queue for sending emails?', 'default' : 'True', 'allowed_values' : ['True', 'False'] },
            ]
        },
        {
            'name' : 'Logging',
            'config_file' : 'logging',
            'config_values' : [
                { 'key' : 'USE_SENTRY', 'prompt' : 'Use Sentry for error logging?', 'default' : 'False', 'allowed_values' : ['True', 'False'] },
                { 'key' : 'SENTRY_DSN', 'prompt' : 'Enter the Sentry DSN', 'show_if' : 'USE_SENTRY', 'show_if_value' : 'True' },
                { 'key' : 'USE_BETTERSTACK', 'prompt' : 'Use Better Stack/Logtail for error logging?', 'default' : 'True', 'allowed_values' : ['True', 'False'] },
                { 'key' : 'BETTERSTACK_SOURCE_TOKEN', 'prompt' : 'Enter the Better Stack source token', 'show_if' : 'USE_BETTERSTACK', 'show_if_value' : 'True' }
            ]
        },
        {
            'name' : 'OpenAI',
            'config_file' : 'openai',
            'config_values' : [
                { 'key' : 'OPENAI_API_KEY', 'prompt' : 'Enter the OpenAI API key', 'default' : None }
            ]
        },
        {
            'name': 'Secrets Manager',
            'config_file': 'secrets',
            'config_values': [
                {
                    'key': 'SECRETS_MANAGER',
                    'prompt': 'Enter the secrets manager to use',
                    'allowed_values': ['infisical', 'aws', 'azure', 'env'],
                    'default': 'env'
                },
                {
                    'key': 'AWS_SECRET_NAME',
                    'prompt': 'Enter the AWS secret name',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'aws',
                },
                {
                    'key': 'AWS_ACCESS_KEY_ID',
                    'prompt': 'Enter the AWS access key ID',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'aws'
                },
                {
                    'key': 'AWS_SECRET_ACCESS_KEY',
                    'prompt': 'Enter the AWS secret access key',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'aws'
                },
                {
                    'key': 'AWS_REGION',
                    'prompt': 'Enter the AWS region',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'aws',
                },
                {
                    'key': 'INFISICAL_PROJECT_ID',
                    'prompt': 'Enter the Infisical project ID',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'infisical'
                },
                {
                    'key': 'INFISICAL_CLIENT_ID',
                    'prompt': 'Enter the Infisical client ID',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'infisical'
                },
                {
                    'key': 'INFISICAL_CLIENT_SECRET',
                    'prompt': 'Enter the Infisical client secret',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'infisical'
                },
                {
                    'key': 'INFISICAL_ENVIRONMENT',
                    'prompt': 'Enter the Infisical environment',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'infisical',
                    'default': 'dev'
                },
                {
                    'key': 'AZURE_CLIENT_ID',
                    'prompt': 'Enter the Azure client ID',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'azure'
                },
                {
                    'key': 'AZURE_TENANT_ID',
                    'prompt': 'Enter the Azure tenant ID',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'azure'
                },
                {
                    'key': 'AZURE_CLIENT_SECRET',
                    'prompt': 'Enter the Azure client secret',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'azure'
                },
                {
                    'key': 'AZURE_KEY_VAULT_NAME',
                    'prompt': 'Enter the Azure Key Vault name',
                    'show_if': 'SECRETS_MANAGER',
                    'show_if_value': 'azure'
                }
            ]
        },
        {
            'name' : 'Languages',
            'config_file' : 'translations',
            'config_values' : [
                { 'key' : 'SOURCE_LANGUAGE_CODE', 'prompt' : 'Enter the default language code', 'default' : 'en-us' },
                { 'key' : 'SOURCE_LANGUAGE_NAME', 'prompt' : 'Enter the default language name', 'default' : 'English' },
            ]
        },
    ]

    def ask_for_input(self, prompt, default = None, allowed_values = None):
        """ Ask the user for input with a default value. Check for allowed values if provided. """

        initial_prompt = prompt

        if default:
            prompt = f'{prompt} (default: {default})'
        
        if allowed_values:
            prompt = f'{prompt} ({", ".join(allowed_values)})'

        value = input(f'{prompt}: ')
        
        if not value and default:
            return default
        
        if allowed_values and value not in allowed_values:
            self.stdout.write(self.style.ERROR(f'Invalid value. Allowed values are: {", ".join(allowed_values)}'))
            return self.ask_for_input(initial_prompt, default, allowed_values)
        
        return value
    
    def get_tmp_answer(self, section, key):
        if section in self.tmp_answers and key in self.tmp_answers[section]:
            return self.tmp_answers[section][key]
        
        return None
    
    def set_tmp_answer(self, section, key, value):
        if section not in self.tmp_answers:
            self.tmp_answers[section] = { key: value }
        else:
            self.tmp_answers[section][key] = value
    
    def handle(self, *args, **options):
        self.tmp_answers = {}

        self.stdout.write(self.style.SUCCESS('''SHIP WITH DJANGO - A Django base for building web applications\n\nWelcome to the Ship With Django project configuration setup! We'll ask you a few questions to configure the project and then you'll be good to go!\nFor each section, you can press Enter to use the default value (if available).\nBe sure to check the documentation for more information on each configuration option.\n'''))
        
        for section in self.ASK_CONFIG_FOR:
            self.stdout.write(self.style.WARNING(f'\n[~] {section["name"]}'))

            for config in section['config_values']:

                # Check if the config should be shown based on another config value
                show_if = config.get('show_if', None)
                show_if_value = config.get('show_if_value', None)

                if show_if:
                    answer = self.get_tmp_answer(section['config_file'], show_if)

                    if show_if_value != answer:
                        continue
                
                # Get the input from the user
                key = config['key']
                prompt = config['prompt']
                default = config.get('default', None)
                allowed_values = config.get('allowed_values', None)
                value = self.ask_for_input(prompt, default, allowed_values)

                # Update the config file with the new value
                # if value is not None:
                #     set_config_value(section['config_file'], key, value)

                # Update the temporary answers for conditional checks
                self.set_tmp_answer(section['config_file'], key, value)

        self.stdout.write(self.style.SUCCESS('Project configuration setup complete!'))