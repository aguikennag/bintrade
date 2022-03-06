from django.urls import include,path
from .transaction import Deposit,Withdrawal,DepositComplete,Invest


urlpatterns = [
    path('withdraw/',Withdrawal.as_view(),name ='withdraw'),
    path('invest/',Invest.as_view(),name ='plans'),
    path('<slug:slug>/deposit/',Deposit.as_view(),name ='deposit'),
    path('<slug:slug>/<str:coin>/invest/<int:amount>/payment-complete/',DepositComplete.as_view(),name ='payment-complete'),
    
]