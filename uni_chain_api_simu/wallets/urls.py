from django.urls import path, include
from .views import WalletTopUp, InstitutionsRegistered, IssuePayToken

urlpatterns = [
    path('wallets/topup/', WalletTopUp.as_view(), name="wallet-topup"),
    path('institutions/', InstitutionsRegistered.as_view(), name='institutions'),
    path('institutions/request_pay_token/', IssuePayToken.as_view(), name='institution_pay_token')
]