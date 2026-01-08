from modules.secrets.base import SecretManager

class EnvSecretManager(SecretManager):
    """ Manages secrets from env file. 
        Secrets are cached in the secrets attribute and can be accessed with the get_secret method.

        When a secret is updated, the cache is NOT updated.
        This means that the application needs to be restarted to get the new value.
    """

secret_manager = EnvSecretManager()