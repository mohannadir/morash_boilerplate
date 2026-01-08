from modules.secrets import secret_manager

STRIPE_LIVE_MODE = secret_manager.get_secret('STRIPE_LIVE_MODE')

STRIPE_LIVE_PUBLIC_KEY = secret_manager.get_secret('STRIPE_PUBLIC_API_KEY')
STRIPE_LIVE_SECRET_KEY = secret_manager.get_secret('STRIPE_SECRET_API_KEY')

STRIPE_TEST_PUBLIC_KEY = secret_manager.get_secret('STRIPE_TEST_PUBLIC_API_KEY')
STRIPE_TEST_SECRET_KEY = secret_manager.get_secret('STRIPE_TEST_SECRET_API_KEY')

STRIPE_TEST_WEBHOOK_SECRET = secret_manager.get_secret('STRIPE_TEST_WEBHOOK_SECRET')
STRIPE_LIVE_WEBHOOK_SECRET = secret_manager.get_secret('STRIPE_WEBHOOK_SECRET')