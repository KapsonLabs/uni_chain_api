from rest_framework import serializers

from .models import Wallet, WalletTransactions

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
    wallet_number = serializers.CharField(max_length=9)
    amount_to_load  = serializers.CharField(max_length=10)

    def validate_amount_number(self, value):
        if len(value) != 8:
           raise serializers.ValidationError("Invalid/wrong account number entered")
        return value 

class WalletDetailsSeriliazer(serializers.ModelSerializer):
    """
    A wallet details serializer
    """

    class Meta:
        model = Wallet
        fields = ('wallet_number', 'wallet_balance')

class WalletTransactionsSerializer(serializers.ModelSerializer):
    """
    A wallet transactions seriliazer for wallet transactions
    """

    class Meta:
        model = WalletTransactions
        fields = ('transaction_type','transaction_amount',)