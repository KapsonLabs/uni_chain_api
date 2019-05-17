from rest_framework import generics
from django.http import QueryDict
import datetime

from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions

from accounts.permissions import StudentPermissions, EmployerPermissions
from .models import Wallet, WalletTransactions
from certificates.models import CertificateFeesSettings
from .serializers import WalletNumberSerializer, WalletTransactionsSerializer, WalletDetailsSeriliazer, PayTokensSerializer, WalletTransactionsDetailSerializer, PayTokenAddressSerializer, PayTokensDetailSerializer

from .helpers import generate_pay_id, generate_transaction_id

class WalletTopUp(generics.CreateAPIView):
    """
    Withdraw savings from account
    """
    permission_classes = (permissions.IsAuthenticated, StudentPermissions, )

    def post(self, request):
        wallet_top_up = WalletNumberSerializer(data=request.data)
        if wallet_top_up.is_valid():
            try:
                related_wallet = Wallet.objects.get(wallet_address=wallet_top_up.data['wallet_address'])

                admin_wallet   =  Wallet.objects.get(wallet_address='1EBEQXDxnibw7o4NMNT7M4HScuG6ZBhB3L')

                admin_wallet_update = {
                    "wallet_balance": float(admin_wallet.wallet_balance)-float(wallet_top_up.data['amount_to_load']),
                }

                wallet_amount_update = {
                    "wallet_balance": float(related_wallet.wallet_balance)+float(wallet_top_up.data['amount_to_load']),
                }

                Wallet.objects.update_or_create(
                            id=admin_wallet.pk, defaults=admin_wallet_update)

                Wallet.objects.update_or_create(
                            id=related_wallet.pk, defaults=wallet_amount_update)

                related_wallet_updated = Wallet.objects.get(wallet_address=wallet_top_up.data['wallet_address'])

                transaction = {
                    "output_wallet_address":admin_wallet.pk,
                    "input_wallet_address":related_wallet_updated.pk,
                    "transaction_type":'TOP-UP',
                    "transaction_amount":wallet_top_up.data['amount_to_load'],
                }

                wallet_transaction = WalletTransactionsSerializer(data=transaction)
                wallet_transaction.is_valid(raise_exception=True)
                wallet_transaction.save()

                transaction_details = {
                    "output_wallet_address":'1EBEQXDxnibw7o4NMNT7M4HScuG6ZBhB3L',
                    "input_wallet_address":related_wallet_updated.wallet_address,
                    "transaction_type":'TOP-UP',
                    "transaction_amount":wallet_top_up.data['amount_to_load'],
                }

                wallet_details = WalletDetailsSeriliazer(related_wallet_updated)
                # wallet_details.is_valid(raise_exception=True)

                transaction_details_json = WalletTransactionsDetailSerializer(transaction_details)

                data_dict = {"status":201, "wallet_details":wallet_details.data, "transaction_details":transaction_details_json.data}
                return Response(data_dict, status=status.HTTP_201_CREATED)

            except:
                data_dict = {"status":404, "error":"Invalid address, Please dont create ur own addresses"}
                return Response(data_dict, status=status.HTTP_404_NOT_FOUND)
        return Response(wallet_top_up.errors, status=status.HTTP_400_BAD_REQUEST)


class InstitutionsRegistered(APIView):

    permission_classes = (permissions.IsAuthenticated, StudentPermissions)

    def get(self, request, format=None):
        wallets = Wallet.objects.filter(is_institution_wallet=True)
        serializer = WalletDetailsSeriliazer(wallets, many=True)
        related_links = 'links'
        data_dict = {"status":200, "links":related_links, "data":serializer.data}
        return Response(data_dict, status=status.HTTP_200_OK)

class IssuePayToken(generics.CreateAPIView):
    
    permission_classes = (permissions.IsAuthenticated, StudentPermissions)

    def post(self, request):
        addresses = PayTokenAddressSerializer(data=request.data)
        if addresses.is_valid():
            student_wallet      = Wallet.objects.get(wallet_address=addresses.data['student_wallet_address'])
            institution_wallet  = Wallet.objects.get(wallet_address=addresses.data['institution_wallet_address'])

            transaction_id = generate_transaction_id()
            
            pay_id         = generate_pay_id(transaction_id, student_wallet.wallet_public_key)

            token_data = {
                    "issued_to_address":student_wallet.pk,
                    "issuer_address":institution_wallet.pk,
                    "token_issued":pay_id,
                    "expected_token_cost":2000,
                    "date_to_expire":datetime.datetime.now()+datetime.timedelta(days=3),
                    "transaction_id_generated":str(transaction_id),
                }

            token_issued = PayTokensSerializer(data=token_data)
            token_issued.is_valid(raise_exception=True)
            token_issued.save()   

            token_details = {
                "token_issued":pay_id,
                "token_expected_amount":2000,
                "token_expiry_date":datetime.datetime.now()+datetime.timedelta(days=3),
            }

            token_details_json = PayTokensDetailSerializer(token_details)       

            data_dict = {"status":201, "token_data":token_details_json.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(addresses.errors, status=status.HTTP_400_BAD_REQUEST)



