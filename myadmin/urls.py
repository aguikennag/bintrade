from django.urls import path,include
from .dashboard import Dashboard,Members,Settings
from .members import MemberDetail
from .investment import CreatePlan,AllPlans,DepositNotice,ApproveDeposit,WithdrawalRequest
from .wallet import  AddCoin,CoinList,DeleteCoin,EditCoin
from .transaction import CreateTransaction,TransactionHistory
from .email import SendCustomMail
from .accounts import Register,Subscribe
from .views import TOS


urlpatterns = [
    #DASHBOARD
    path('',Dashboard.as_view(),name = 'admin-dashboard'),
    path('members/',Members.as_view(),name = 'my-members'),
    path('member/<str:username>',Members.as_view(),name = 'member-detail'),
    path('settings/',Settings.as_view(),name = 'admin-settings'),
    path('bfybydbfbbdhbfsbdgfgbgfgsvfg2ry/',Register.as_view(),name='admin-register'),
    path('Terms-of-service',TOS.as_view(),name = 'tos'),

    #MEMBERS
    path('member/<str:username>/',MemberDetail.as_view(),name = 'member-detail'),
    


    #PLAN
    path('plans/create/',CreatePlan.as_view(),name = 'create-plan'),
    path('plans/delete/',AllPlans.as_view(),name='delete-plan'),
    path('plans/',AllPlans.as_view(),name='plans-admin'),

    #DEPOSIT
    path('deposit-notice/',DepositNotice.as_view(),name='deposit-notice'),
    path('deposit-notice/approve/',ApproveDeposit.as_view(),name='approve-deposit'),
    
    
    #COIN
    path('coin-address/add/',AddCoin.as_view(),name='add-coin'),
    path('coin-address/delete/',DeleteCoin.as_view(),name='delete-coin'),
    path('coin-address/edit/',EditCoin.as_view(),name='edit-coin'),
    path('coin-address/',CoinList.as_view(),name='coin-list'),

    #TRANSACTION
    path('transaction/create/<str:wallet_id>/',CreateTransaction.as_view(),name='create-transaction'),
    path('transactions/',TransactionHistory.as_view(),name = 'transaction-history'),
    path('withdrawals/',WithdrawalRequest.as_view(),name = 'withdrawals'),

    #EMAIL
    path('mail/send-custom-email/<str:wallet_id>/',SendCustomMail.as_view(),name='send-custom-mail'),
    
    #SUBSCRIPTION
    path('subscribe/',Subscribe.as_view(),name='subscibe-admin')
    
]