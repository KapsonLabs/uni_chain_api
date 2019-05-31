from django.urls import path, include
from .views import WalletTopUp, InstitutionsRegistered, IssuePayToken, WalletBalance, WalletTransactionHistory, WalletEscrowTransactions, PredictData

urlpatterns = [
    path('wallets/topup/', WalletTopUp.as_view(), name="wallet-topup"),
    path('institutions/', InstitutionsRegistered.as_view(), name='institutions'),
    path('institutions/request_pay_token/', IssuePayToken.as_view(), name='institution_pay_token'),
    path('wallets/balance/', WalletBalance.as_view(), name='wallet_balances'),
    path('wallets/transaction_history/', WalletTransactionHistory.as_view(), name='wallet_transactions'),
    path('institutions/escrow_transactions/', WalletEscrowTransactions.as_view(), name='instituions_escrow'),
    path('predict_data/', PredictData.as_view(), name='predict_data'),
]