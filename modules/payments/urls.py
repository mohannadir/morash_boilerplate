from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('webhook/stripe/', views.StripeWebhook.as_view(), name='stripe_webhook'),

    path('checkout/price/<str:price_id>/', views.SetupCheckoutForPrice.as_view(), name='setup_checkout_for_price'),
    path('checkout/complete/', views.CheckoutComplete.as_view(), name='checkout_complete'),
    path('checkout/cancelled/', views.CheckoutCancelled.as_view(), name='checkout_cancelled'),
]