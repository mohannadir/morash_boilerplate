from django.contrib import admin
from django.urls import path, include
import modules.authentication.views as views

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('forgot-password/', views.UserForgotPassword.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.UserResetPassword.as_view(), name='reset_password'),
    path('change-password/', views.UserChangePassword.as_view(), name='change_password'),

    path('activate/<uidb64>/<token>/', views.UserActivate.as_view(), name='activate_user'),

    path('settings/', views.UserSettings.as_view(), name='user_settings'),
]