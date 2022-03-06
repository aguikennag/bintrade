from  django.urls import path,include
from .views import Subscribe
from .accounts import Register,LoginRedirect
from .dashboard import KYC, Dashboard,Profile, Referral, Setting, Transaction

urlpatterns = [
    path('subscribe/',Subscribe.as_view(),name = 'subscribe'),
    path('register/',Register.as_view(),name = 'register'),
    path('dashboard/',Dashboard.as_view(),name = 'dashboard'),
    path('profile/',Profile.as_view(),name = 'profile'),
    path('kyc/',KYC.as_view(),name = 'kyc'),
    path('settings/',Setting.as_view(),name = 'setting'),
    path('transactions/',Transaction.as_view(),name = 'transaction'),
    path('referral/',Referral.as_view(),name = 'referral'),
    path('login-redirect/',LoginRedirect.as_view(),name="login-redirect")


    #path('profile/',Profile.as_view(),name = 'register'),
    

]