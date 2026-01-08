from modules.secrets import secret_manager

OPENAI_API_KEY = secret_manager.get_secret('OPENAI_API_KEY')