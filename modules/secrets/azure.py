from modules.secrets.base import SecretManager
from CONFIG.secrets import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_KEY_VAULT_NAME
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

class AzureSecretManager(SecretManager):
    """ Manages secrets from Azure Key Vault. 
        Secrets are cached in the secrets attribute and can be accessed with the get_secret method.

        When a secret is updated in Azure, the cache is NOT updated.
        This means that the application needs to be restarted to get the new value.
    """

    def setup(self):
        self.with_external_provider = True
        self.credential = ClientSecretCredential(tenant_id=AZURE_TENANT_ID, client_id=AZURE_CLIENT_ID, client_secret=AZURE_CLIENT_SECRET)
        self.client = SecretClient(vault_url=f"https://{AZURE_KEY_VAULT_NAME}.vault.azure.net/", credential=self.credential)
    
    def get_all_provider_secrets(self):
        """ Returns all secrets from Azure Key Vault. """

        azure_secrets = {}
        secret_properties = self.client.list_properties_of_secrets()
        for secret_property in secret_properties:
            secret_name = secret_property.name
            secret = self.client.get_secret(secret_name)
            azure_secrets[secret_name] = secret.value

        parsed_secrets = {}
        for key, value in azure_secrets.items():
            parsed_secrets[key] = self.parse_value(value)

        return parsed_secrets

secret_manager = AzureSecretManager()