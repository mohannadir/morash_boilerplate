from django.contrib import admin
from django.urls import path, include

import {{ cookiecutter.main_app_name }}.views as views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
]