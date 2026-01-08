from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('check-file-task-status/<str:task_id>/', views.HueyCheckFileTaskStatus.as_view(), name='check-file-task-status'),
]