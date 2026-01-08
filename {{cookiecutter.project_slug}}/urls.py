from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include(('{{ cookiecutter.main_app_name }}.urls', '{{ cookiecutter.main_app_name }}'), namespace='{{ cookiecutter.main_app_name }}')),
    path('api/', include(('api.urls', 'api'), namespace='api')),

    path('i18n/', include('django.conf.urls.i18n')), # Internationalization/translation
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"), # Internationalization/translation for JS
    path('swd/', include('modules.urls')), # Ship with Django
    
    path("__reload__/", include("django_browser_reload.urls")),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]