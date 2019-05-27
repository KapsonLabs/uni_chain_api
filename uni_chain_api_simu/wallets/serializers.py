from rest_framework import serializers

from .models import Wallet, WalletTransactions, PayTokens, EscrowTransactions
from accounts.serializers import UserDetailSerializer
from certificates.serializers import AddressSerializer, DocumentUploadSerializer
from certificates.models import CertificateViewRequests

class WalletsSerializer(serializers.ModelSerializer):
    """
    A serialiser that creates an automatic wallet
    """
    class Meta:
        model = Wallet
        fields = ('wallet_number','wallet_private_key', 'wallet_address', 'wallet_public_key')

class WalletNumberSerializer(serializers.Serializer):
    """
    A wallet number serializer for checking statuses
    """
    wallet_address = serializers.CharField(max_length=250)
    amount_to_load  = serializers.CharField(max_length=10)

class WalletAddressSerializer(serializers.ModelSerializer):
    """
    A wallet address serializer
    """
    class Meta:
        model = Wallet
        fields = ('wallet_address', )

    # def validate_amount_number(self, value):
    #     if len(value) != 8:
    #        raise serializers.ValidationError("Invalid/wrong account number entered")
    #     return value 

class WalletBalanceSerializer(serializers.ModelSerializer):
    """
    A wallet balance serializer
    """

    class Meta:
        model=Wallet
        fields=('wallet_balance',)

class WalletDetailsSeriliazer(serializers.ModelSerializer):
    """
    A wallet details serializer
    """

    wallet_owner = UserDetailSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = ('wallet_owner' ,'wallet_address', 'wallet_public_key', 'wallet_balance')

class WalletTransactionsSerializer(serializers.ModelSerializer):
    """
    A wallet transactions seriliazer for wallet transactions
    """

    class Meta:
        model = WalletTransactions
        fields = ('transaction_type','transaction_amount', 'output_wallet_address', 'input_wallet_address', 'transaction_id')

class WalletTransactionsDetailSerializer(serializers.Serializer):
    """
    A wallet transaction detail seriliazer
    """
    output_wallet_address       = serializers.CharField(max_length=255)
    input_wallet_address        = serializers.CharField(max_length=255)
    transaction_type            = serializers.CharField(max_length=255)
    transaction_amount          = serializers.DecimalField(max_digits=20, decimal_places=3)
    transaction_id              = serializers.CharField(max_length=255)

class EscrowTransactionDetailSerializer(serializers.Serializer):
    """
    An escrow transaction detail seriliazer
    """
    output_wallet_address       = serializers.CharField(max_length=255)
    input_wallet_address        = serializers.CharField(max_length=255)
    transaction_type            = serializers.CharField(max_length=255)
    transaction_id              = serializers.CharField(max_length=255)
    transaction_amount          = serializers.DecimalField(max_digits=20, decimal_places=3)

class PayTokenAddressSerializer(serializers.Serializer):
    """
    A pay token serializer for creating the token
    """
    student_wallet_address      = serializers.CharField(max_length=255)
    institution_wallet_address  = serializers.CharField(max_length=255)

class PayTokensSerializer(serializers.ModelSerializer):
    """
    A payment token serializer for issuing and saving payment tokens
    """

    class Meta:
        model = PayTokens
        fields=('issued_to_address', 'issuer_address', 'token_issued', 'expected_token_cost', 'date_to_expire', 'transaction_id_generated')

class PayTokensDetailSerializer(serializers.Serializer):
    """
    A pay token detail seriliazer
    """
    token_issued                        = serializers.CharField(max_length=255)
    token_expected_amount               = serializers.DecimalField(max_digits=20, decimal_places=3)
    token_expiry_date                   = serializers.DateTimeField()

class DocumentVerificationRequestSerializer(serializers.ModelSerializer):
    """
    A document verification request serializer
    """

    # document_id         = DocumentUploadSerializer(read_only=True)
    # verifying_entity    = WalletAddressSerializer(read_only=True)
    # requesting_entity   = WalletAddressSerializer(read_only=True)

    class Meta:
        model = CertificateViewRequests
        fields = ("id", "document_id","verifying_entity","requesting_entity")


class DocumentVerificationRequestDataSerializer(serializers.ModelSerializer):
    """
    A document verification request serializer
    """

    document_id         = DocumentUploadSerializer(read_only=True)
    verifying_entity    = WalletAddressSerializer(read_only=True)
    requesting_entity   = WalletAddressSerializer(read_only=True)

    class Meta:
        model = CertificateViewRequests
        fields = ("id", "document_id","verifying_entity","requesting_entity")
        

class EscrowTransactionsSerializer(serializers.ModelSerializer):
    """
    A serializer for escrow transactions
    """
    # output_wallet_address   = WalletAddressSerializer()
    # input_wallet_address    = WalletAddressSerializer()

    class Meta:
        model = EscrowTransactions
        fields = ("output_wallet_address","input_wallet_address","transaction_id","transaction_type","amount_initiated")

class WalletTransactionsHistorySerialiazer(serializers.ModelSerializer):
    """
    A wallet serialiazer to serialize wallet histroy transactions
    """
    output_wallet_address   = WalletAddressSerializer(read_only=True)
    input_wallet_address    = WalletAddressSerializer(read_only=True)

    class Meta:
        model = WalletTransactions
        fields = ('output_wallet_address', 'input_wallet_address', 'transaction_id', 'transaction_type', 'transaction_amount', 'date_transacted')

