from modules.secrets import secret_manager

# Minimal configuration for the Huey task queue.
# If you need advanced configuration, you will need to edit the "HUEY" dictionary in the settings.py file.
# See https://huey.readthedocs.io/en/latest/django.html for more information.

HUEY_CLASS = 'huey.PriorityRedisHuey'
REDIS_HOST = secret_manager.get_secret('REDIS_HOST')
REDIS_PORT = 6379