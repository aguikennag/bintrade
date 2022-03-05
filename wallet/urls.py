from django.urls import include,path
from .transaction import Deposit,Withdrawal,DepositComplete,Invest,EnterDepositAmount


urlpatterns = [
    path('withdraw/',Withdrawal.as_view(),name ='withdraw'),
    path('invest/',Invest.as_view(),name ='plans'),
    path('<slug:slug>/invest/<int:amount>',Deposit.as_view(),name ='deposit'),
    path('<slug:slug>/invest/enter-amount',EnterDepositAmount.as_view(),name ='enter-amount'),
    path('<slug:slug>/<str:coin>/invest/<int:amount>/payment-complete/',DepositComplete.as_view(),name ='payment-complete'),
    
]