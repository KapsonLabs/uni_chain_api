from django.contrib import admin
from .models import Wallet, EscrowTransactions, PayTokens, WalletTransactions

admin.site.register(Wallet)
admin.site.register(EscrowTransactions)
admin.site.register(PayTokens)
admin.site.register(WalletTransactions)
