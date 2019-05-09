from rest_framework import generics
from django.http import QueryDict

from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions

from accounts.permissions import StudentPermissions, EmployerPermissions
from .models import Wallet, WalletTransactions
from .serializers import WalletNumberSerializer, WalletTransactionsSerializer, WalletDetailsSeriliazer

class WalletTopUp(generics.CreateAPIView):
    """
    Withdraw savings from account
    """
    permission_classes = (permissions.IsAuthenticated, StudentPermissions, )

    def post(self, request):
        wallet_top_up = WalletNumberSerializer(data=request.data)
        if wallet_top_up.is_valid():
            related_wallet = Wallet.objects.get(wallet_number=wallet_top_up.data['wallet_number'])

            wallet_amount_update = {
                "wallet_balance": float(related_wallet.wallet_balance)+float(wallet_top_up.data['amount_to_load']),
            }

            Wallet.objects.update_or_create(
                        id=related_wallet.pk, defaults=wallet_amount_update)

            related_wallet_updated = Wallet.objects.get(wallet_number=wallet_top_up.data['wallet_number'])

            transaction_details = {
                "transaction_type":'TOP-UP',
                "transaction_amount":wallet_top_up.data['amount_to_load'],
            }

            wallet_transaction = WalletTransactionsSerializer(data=transaction_details)
            wallet_transaction.is_valid(raise_exception=True)
            wallet_transaction.save(related_wallet=related_wallet)

            wallet_details = WalletDetailsSeriliazer(related_wallet_updated)
            # wallet_details.is_valid(raise_exception=True)

            data_dict = {"status":201, "wallet_details":wallet_details.data, "transaction_details":wallet_transaction.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)

        return Response(wallet_top_up.errors, status=status.HTTP_400_BAD_REQUEST)


