import boto3
import json
from modules.secrets.base import SecretManager
from CONFIG.secrets import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_SECRET_NAME

class AWSSecretManager(SecretManager):
    """ Manages secrets from AWS. 
        Secrets are cached in the secrets attribute and can be accessed with the get_secret method.

        When a secret is updated in AWS, the cache is NOT updated.
        This means that the application needs to be restarted to get the new value.
    """

    def setup(self):
        self.with_external_provider = True
        self.session = boto3.session.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

        self.client = self.session.client('secretsmanager')
    
    def get_all_provider_secrets(self):
        """ Returns all secrets from AWS. """

        aws_secrets = json.loads(self.client.get_secret_value(SecretId=AWS_SECRET_NAME)['SecretString'])

        parsed_secrets = {}
        for key, value in aws_secrets.items():
            parsed_secrets[key] = self.parse_value(value)
        
        return parsed_secrets

secret_manager = AWSSecretManager()