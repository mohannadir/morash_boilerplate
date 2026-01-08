from modules.secrets.base import SecretManager
from infisical_client import ClientSettings, InfisicalClient, ListSecretsOptions
from CONFIG.secrets import INFISICAL_CLIENT_ID, INFISICAL_CLIENT_SECRET, INFISICAL_ENVIRONMENT, INFISICAL_PROJECT_ID

class InfisicalSecretManager(SecretManager):
    """ Manages secrets from Infiscal. 
        Secrets are cached in the secrets attribute and can be accessed with the get_secret method.

        When a secret is updated in Infisical, the cache is NOT updated.
        This means that the application needs to be restarted to get the new value.
    """

    def setup(self):
        self.with_external_provider = True
        self.client = InfisicalClient(ClientSettings(
            client_id=INFISICAL_CLIENT_ID,
            client_secret=INFISICAL_CLIENT_SECRET
        ))
    
    def get_all_provider_secrets(self):
        infisical_secrets = self.client.listSecrets(options=ListSecretsOptions(
            environment=INFISICAL_ENVIRONMENT,
            project_id=INFISICAL_PROJECT_ID
        ))

        parsed_secrets = {}
        for secret in infisical_secrets:
            parsed_secrets[secret.secret_key] = self.parse_value(secret.secret_value)
        
        return parsed_secrets

secret_manager = InfisicalSecretManager()