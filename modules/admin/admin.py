from django.contrib import admin

# We start with unregistering models we do not need
# These can be re-registered using Unfold if necessary
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(Group)
admin.site.unregister(Site)
