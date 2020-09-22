from django.urls import path

from accounts.views import *

urlpatterns = [
    path('sign-in-request', SignInRequestView.as_view(), name='SignInRequest')
]
#     path('sign-up-as-company', SignUpAsCompanyView.as_view(), name='signUpAsCompany'),
#     path('sign-in', SignInView.as_view(), name='signIn'),
#     path('forgot-password', ForgotPasswordView.as_view(), name='forgotPassword'),
#     path('reset-password', ResetPasswordView.as_view(), name='resetPassword'),
#     path('change-password', ChangePasswordView.as_view(), name='changePassword'),
#     path('profile', ProfileView.as_view(), name='getOrUpdateUserProfile'),
# ]
