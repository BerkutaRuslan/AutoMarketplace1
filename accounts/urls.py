from django.urls import path

from accounts.views import *

urlpatterns = [
    path('sign-in-request', SignInRequestView.as_view(), name='SignInRequest'),
    path('sign-in-verify', SignInVerifyView.as_view(), name='signInVerify'),
    path('profile/setup', UserProfileSetupView.as_view(), name='updateUser'),
    path('profile', UserProfileView.as_view(), name='getUser'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgotPassword'),
    path('reset-password', ResetPasswordView.as_view(), name='resetPassword'),
]
