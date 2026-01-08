# Configuration for Django Rosetta
# https://django-rosetta.readthedocs.io/en/latest/settings.html

SOURCE_LANGUAGE_CODE = 'en-us'
SOURCE_LANGUAGE_NAME = 'English'
ROSETTA_MESSAGES_PER_PAGE = 100

# List of languages that are able to be translated from the source language
# Translation can be done through the admin panel
# NOTE: these languages are NOT available for users to select on the front end
# They are only available for translation in the admin panel
# If you want to enable them for users to select, you will need to add them to the LANGUAGES setting
# Languages that are in the LANGUAGES setting will automatically be added to the list of available languages for translation
ROSETTA_LANGUAGES = []

# List of languages that are available for users to select on the front end
LANGUAGES = [
    ('en-us', 'English'),
    ('ar', 'Arabic')
]

# API Keys for translation services
YANDEX_TRANSLATE_KEY = None  # See http://api.yandex.com/translate/
AZURE_CLIENT_SECRET = None  # See https://learn.microsoft.com/en-us/azure/ai-services/translator/c
DEEPL_AUTH_KEY = None  # See https://www.deepl.com/pro#developerr
