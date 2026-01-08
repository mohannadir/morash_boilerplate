from modules.secrets import secret_manager

# This variable is used to determine which email provider to use
# This can be either normal SMTP or SendGrid.
# If you want to use SendGrid, set this to 'sendgrid' and set the SENDGRID_API_KEY variable.
EMAIL_PROVIDER = 'smtp' # 'smtp' or 'sendgrid'

# If this variable is set to True, sending emails will be done using the task queue (Huey) instead of the main thread.
# This is useful for sending emails asynchronously. If you set this to True, make sure to run the task queue worker.
# If you set this to False, emails will be sent synchronously and the main thread will be blocked until the email is sent.
EMAIL_USE_TASK_QUEUE = True

EMAIL_HOST = secret_manager.get_secret('EMAIL_HOST')
EMAIL_PORT = secret_manager.get_secret('EMAIL_PORT')
EMAIL_HOST_USER_NAME = secret_manager.get_secret('EMAIL_HOST_USER_NAME')
EMAIL_HOST_USER = secret_manager.get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = secret_manager.get_secret('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = secret_manager.get_secret('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SENDGRID_API_KEY = secret_manager.get_secret('SENDGRID_API_KEY')