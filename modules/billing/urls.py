from django.contrib import admin
from django.urls import path, include
import modules.billing.views as views
from CONFIG.billing import BILLING_MODEL

urlpatterns = [
    path('', views.ManageBilling.as_view(), name='manage_billing'),
    path('cancel-subscription/', views.CancelSubscription.as_view(), name='cancel_subscription'),
    path('subscribe/<str:subscription_key>/', views.SubscripeToSubscription.as_view(), name='subscribe_to_subscription'),

    path('credits/purchase/<str:credit_package_key>/', views.PurchaseCreditsPackage.as_view(), name='purchase_credits_package'),
    path('credits/actions/table/data/', views.CreditActionsTableData.as_view(), name='credit_actions_table'),

     path('invoices/table/data/', views.InvoiceTableData.as_view(), name='invoice_table'),
] if BILLING_MODEL != 'none' else []