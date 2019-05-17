from django.db import models
from accounts.models import User
from .choices import TRANSACTION_TYPES

class Wallet(models.Model):
    wallet_owner            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet_owner')
    wallet_number           = models.CharField(max_length=100, null=True, blank=True)
    wallet_address          = models.CharField(max_length=255, null=True, blank=True)
    wallet_private_key      = models.CharField(max_length=255, null=True, blank=True)
    wallet_public_key       = models.CharField(max_length=255, null=True, blank=True)
    wallet_balance          = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    is_institution_wallet   = models.BooleanField(default=False)   
    date_created            = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.wallet_address)

class WalletTransactions(models.Model):
    output_wallet_address   = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='output_wallet_address', blank=True, null=True)
    input_wallet_address    = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='input_wallet_address', blank=True, null=True)
    transaction_id          = models.CharField(max_length=255, blank=True, null=True)
    transaction_type        = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_amount      = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    date_transacted         = models.DateTimeField(auto_now_add=True)

class PayTokens(models.Model):
    issued_to_address           = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='token_issued_wallet_address')
    issuer_address              = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='token_issuer_wallet_address')
    token_issued                = models.CharField(max_length=400)
    expected_token_cost         = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    transaction_id_generated    = models.CharField(max_length=255, null=True, blank=True)
    token_active                = models.BooleanField(default=True)
    date_to_expire              = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_issued                 = models.DateTimeField(auto_now_add=True)

class EscrowTransactions(models.Model):
    output_wallet_address       = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='escrow_output_wallet_address')
    input_wallet_address        = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='escrow_input_wallet_address')
    transaction_id              = models.CharField(max_length=255, blank=True, null=True)
    transaction_type            = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount_initiated            = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    is_document_verification    = models.BooleanField(default=False)
    is_certificate_view         = models.BooleanField(default=False)
    date_initiated              = models.DateTimeField(auto_now_add=True)
    date_transferred            = models.DateTimeField(auto_now_add=False, null=True, blank=True)

