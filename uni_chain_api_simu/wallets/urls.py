from django.urls import path, include
from .views import WalletTopUp

urlpatterns = [
    path('wallets/topup/', WalletTopUp.as_view(), name="wallet-topup"),
]