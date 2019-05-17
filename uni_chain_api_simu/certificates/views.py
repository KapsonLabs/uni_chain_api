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
from wallets.models import Wallet, WalletTransactions
from .models import CertificateFeesSettings
from .serializers import DocumentRequestVerificationSerializer, DocumentVerificationRequestSerializer
from wallets.serializers import EscrowTransactionsSerializer

from wallets.helpers import generate_pay_id, generate_transaction_id


class RequestCertificateVerification(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, StudentPermissions)

    def post(self, request):
        verification_request = DocumentRequestVerificationSerializer(data=request.data)
        if verification_request.is_valid():
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

