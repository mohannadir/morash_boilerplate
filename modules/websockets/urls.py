from django.urls import path
from . import views

urlpatterns = [
    path('ws/examples/', views.ExampleConsumer.as_asgi(), name='examples'),
    path('ws/users/', views.UserConsumer.as_asgi(), name='users'),
]