from rest_framework import generics
from django.http import QueryDict

from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions

from accounts.permissions import StudentPermissions, EmployerPermissions, InstitutionAdministratorPermissions
from certificates.models import Certificate, CertificateVerificationRequests
# from .serializers import CertificatesSerializer, CertificateVerificationRequestSerializer
from wallets.models import Wallet, WalletTransactions
from wallets.serializers import WalletDetailsSeriliazer, WalletTransactionsSerializer

# class CertificateUpload(generics.CreateAPIView):
#     """
#     Certificate Upload view
#     """
#     permission_classes = (permissions.IsAuthenticated, StudentPermissions, )

#     def post(self, request):
#         certificate = CertificatesSerializer(data=request.data)
#         if certificate.is_valid():
#             certificate.save(certificate_owner=request.user)

#             data_dict = {"status":201, "data":certificate.data}
#             return Response(data_dict, status=status.HTTP_201_CREATED)
#         return Response(certificate.errors, status=status.HTTP_400_BAD_REQUEST)

# class CertificateVerificationRequestView(generics.CreateAPIView):
#     """
#     Certificate Verification Request view
#     """
#     permission_classes = (permissions.IsAuthenticated, StudentPermissions, )

#     def post(self,request):
#         verification_request = CertificateVerificationRequestSerializer(data=request.data)
#         if verification_request.is_valid():
#             verification_request.save(requested_by=request.user)

#             verification = CertificateVerificationRequests.objects.get(pk=verification_request.data['id'])

#             related_wallet = Wallet.objects.get(wallet_owner=verification.requested_by)
            
#             wallet_amount_update = {
#                 "wallet_balance": float(related_wallet.wallet_balance)-float(3000),
#             }

#             Wallet.objects.update_or_create(
#                         id=related_wallet.pk, defaults=wallet_amount_update)

#             related_wallet_updated = Wallet.objects.get(wallet_number=related_wallet.wallet_number)

#             transaction_details = {
#                 "transaction_type":'VERIFICATION',
#                 "transaction_amount":3000,
#             }

#             wallet_transaction = WalletTransactionsSerializer(data=transaction_details)
#             wallet_transaction.is_valid(raise_exception=True)
#             wallet_transaction.save(related_wallet=related_wallet)

#             wallet_details = WalletDetailsSeriliazer(related_wallet_updated)

#             data_dict = {"status":201, "data":verification_request.data, "account_details":wallet_details.data}
#             return Response(data_dict, status=status.HTTP_201_CREATED)
#         return Response(verification_request.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewCertificateVerificationRequests(APIView):
    """
    View verification requests
    """
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions, )

    def get(self,request):
        pass


