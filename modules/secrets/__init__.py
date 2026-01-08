from CONFIG.secrets import SECRETS_MANAGER
if SECRETS_MANAGER == 'infisical':
    from modules.secrets.infisical import secret_manager
elif SECRETS_MANAGER == 'aws':
    from modules.secrets.aws import secret_manager
elif SECRETS_MANAGER == 'azure':
    from modules.secrets.azure import secret_manager
elif SECRETS_MANAGER == 'env':
    from modules.secrets.env import secret_manager
else:
    raise Exception(f"Invalid SECRETS_MANAGER value: {SECRETS_MANAGER}. Valid values are 'infisical', 'aws', 'azure' or 'env'.")

secret_manager = secret_manager