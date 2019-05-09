from django.db import models
from accounts.models import User
from .choices import TRANSACTION_TYPES

class Wallet(models.Model):
    wallet_owner        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet_owner')
    wallet_number       = models.CharField(max_length=100, null=True, blank=True)
    wallet_address      = models.CharField(max_length=255, null=True, blank=True)
    wallet_private_key  = models.CharField(max_length=255, null=True, blank=True)
    wallet_public_key   = models.CharField(max_length=255, null=True, blank=True)
    wallet_balance      = models.DecimalField(max_digits=20, decimal_places=3, default=0)  
    date_created        = models.DateTimeField(auto_now_add=True)

class WalletTransactions(models.Model):
    related_wallet      = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='related_wallet')
    transaction_type    = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_amount  = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    date_transacted     = models.DateTimeField(auto_now_add=True)
