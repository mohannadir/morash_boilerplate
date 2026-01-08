
# Determines which service to use for secrets management. Values can be 'infisical', 'aws', 'azure' or 'env'.
# If 'env' is used, secrets will be read from the .env.example file.
# NOTE: When requesting a secret using the secrets manager, the manager will ALWAYS look at the .env.example file first and return the value if it exists.
# If it does not exist, only then it will look at the configured external service (if any). This is to easily override secrets for local development or testing.

SECRETS_MANAGER = 'env' 

# When using AWS Secrets Manager, the following variables are required.
AWS_SECRET_NAME = None
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None
AWS_REGION = None

# When using Infisical, the following variables are required.
INFISICAL_PROJECT_ID = None
INFISICAL_CLIENT_ID = None
INFISICAL_CLIENT_SECRET = None
INFISICAL_ENVIRONMENT = None

# When using Azure Key Vault, the following variables are required.
AZURE_CLIENT_ID = None
AZURE_TENANT_ID = None
AZURE_CLIENT_SECRET = None
AZURE_KEY_VAULT_NAME = None