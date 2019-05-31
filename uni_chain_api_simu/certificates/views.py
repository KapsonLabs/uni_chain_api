from rest_framework import generics
from django.http import QueryDict
import datetime

from django.http import Http404
from rest_framework.views import APIView
from accounts.models import User
from django.db.models import Avg, Count, Min, Sum

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from accounts.permissions import StudentPermissions, EmployerPermissions, InstitutionAdministratorPermissions
from wallets.models import Wallet, WalletTransactions, PayTokens, EscrowTransactions
from .models import CertificateFeesSettings, CertificateViewRequests, Documents, Certificate
from .serializers import DocumentRequestVerificationSerializer, DocumentUploadSerializer, AddressSerializer, CertificateUploadSerializer, CertificateDetailSerializer, CertificateGrantAccessSerializer, CertificateGrantedAccessSerializer
from wallets.serializers import EscrowTransactionsSerializer, EscrowTransactionDetailSerializer, DocumentVerificationRequestSerializer, WalletTransactionsSerializer, DocumentVerificationRequestDataSerializer, WalletTransactionsSerializer

from wallets.helpers import generate_pay_id, generate_transaction_id, decode_pay_id
from .helpers import generate_certificate_link


class RequestCertificateVerification(generics.CreateAPIView):
    # parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated, StudentPermissions)

    def post(self, request):
        file_data = request.data.copy()

        student_address     = file_data.pop('student_address', None)[0]
        public_key          = file_data.pop('public_key', None)[0]
        pay_token           = file_data.pop('pay_token', None)[0]

        file_request = DocumentUploadSerializer(data=file_data)
        if file_request.is_valid():
            #decode payment token with the public key provided
            token_data = PayTokens.objects.get(token_issued=pay_token)

            if token_data.token_active==True:
                try:
                    decoded_data = decode_pay_id(pay_token, public_key)
                    print(decoded_data)

                    student_wallet      = Wallet.objects.get(wallet_address=student_address)
                    institution_wallet  = Wallet.objects.get(wallet_address=decoded_data['inst_address'])
                    print(institution_wallet.pk)
                    
                    #invalidate token after it has been decoded
                    token_update={
                        "token_active": False,
                    }

                    PayTokens.objects.update_or_create(
                            id=token_data.pk, defaults=token_update)
                    
                    #move money from the student's account
                    student_wallet_amount_update = {
                        "wallet_balance": float(student_wallet.wallet_balance)-float(2000),
                    }

                    Wallet.objects.update_or_create(
                            id=student_wallet.pk, defaults=student_wallet_amount_update)

                    # related_wallet_updated = Wallet.objects.get(wallet_address=wallet_top_up.data['wallet_address'])

                    #move money to escrow account
                    escrow_data = {
                        "output_wallet_address":student_wallet.pk,
                        "input_wallet_address":institution_wallet.pk,
                        "transaction_id":decoded_data['txn_id'],
                        "transaction_type":"VERIFICATION",
                        "amount_initiated":2000,
                    }

                    print(escrow_data)

                    escrow_data_save = EscrowTransactionsSerializer(data=escrow_data)
                    escrow_data_save.is_valid(raise_exception=True)
                    escrow_data_save.save(is_document_verification=True) 

                    #save the document
                    file_request.save(document_owner=student_wallet)

                    # document_data_save = DocumentUploadSerializer(data=document_data)
                    # document_data_save.is_valid(raise_exception=True)
                    # document_data_save.save()

                    #create the request at the institution end
                    document_verification_data = {
                        "document_id":file_request.data['id'],
                        "verifying_entity":institution_wallet.pk,
                        "requesting_entity":student_wallet.pk,
                        "escrow_transaction_related":escrow_data_save.data['id']
                    }

                    document_verification_data_save = DocumentVerificationRequestSerializer(data=document_verification_data)
                    document_verification_data_save.is_valid(raise_exception=True)
                    document_verification_data_save.save(is_document_verification=True)

                    escrow_data_detail = {
                        "output_wallet_address":student_wallet.wallet_address,
                        "input_wallet_address":institution_wallet.wallet_address,
                        "transaction_id":escrow_data_save.data['transaction_id'],
                        "transaction_type":escrow_data_save.data['transaction_type'],
                        "transaction_amount":escrow_data_save.data['amount_initiated'],
                    }

                    escrow_data_detail_json = EscrowTransactionDetailSerializer(escrow_data_detail)

                    data_dict = {"status":201, "txn_data":escrow_data_detail_json.data}
                    return Response(data_dict, status=status.HTTP_201_CREATED)
                except:
                    return Response({"status":400, "error":"Token invalid or has already been used 1"},status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"status":400, "error":"Token invalid or has already been used"},status=status.HTTP_400_BAD_REQUEST)
        return Response(file_request.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationRequests(APIView):
    
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)

    def post(self, request):
        institution_address = AddressSerializer(data=request.data)
        if institution_address.is_valid():
            institution_wallet  = Wallet.objects.get(wallet_address=institution_address.data['wallet_address'])

            verification_requests = CertificateViewRequests.objects.filter(verifying_entity=institution_wallet.pk).filter(is_document_verification=True)
            verification_serializer = DocumentVerificationRequestDataSerializer(verification_requests, many=True)

            data_dict = {"status":200, "data":verification_serializer.data}
            return Response(data_dict, status=status.HTTP_200_OK)
        return Response(institution_address.errors, status=status.HTTP_400_BAD_REQUEST)


# class ViewEscrowAmount(APIView):
    
#     permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)

#     def post(self, request):
#         institution_address = AddressSerializer(data=request.data)
#         if institution_address.is_valid():
#             institution_wallet  = Wallet.objects.get(wallet_address=institution_address.data['institution_wallet_address'])

#             escrow_amount = Wallet.objects.get(wallet_address=institution_wallet.pk).aggregate(account_balance=Sum('account_balance'))

#             verification_serializer = DocumentVerificationRequestSerializer(escrow_amount)

#             data_dict = {"status":200, "data":verification_serializer.data}
#             return Response(data_dict, status=status.HTTP_200_OK)
#         return Response(institution_address.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifiedCertificateUpload(APIView):

    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)
    
    def post(self, request):
        certificate_data     = request.data.copy()

        document_id          = certificate_data.pop('document_id', None)[0]
        verification_status  = certificate_data.pop('verification_status', None)[0]

        certificate = CertificateUploadSerializer(data=certificate_data)
        if certificate.is_valid():
            #try:
            #change document status being verified
            related_document = CertificateViewRequests.objects.get(id=int(document_id))

            if related_document.verification_view_status == False:
            
                document_status_update = {
                        "verification_view_status": True,
                    }

                CertificateViewRequests.objects.update_or_create(
                    id=related_document.pk, defaults=document_status_update)

                #move money from escrow to the wallet address of the institution
                escrow_transaction = EscrowTransactions.objects.get(pk=related_document.escrow_transaction_related.pk)

                escrow_transaction_update = {
                    "escrow_active": False,
                    "date_transferred":datetime.datetime.now()
                }

                EscrowTransactions.objects.update_or_create(
                    id=escrow_transaction.pk, defaults=escrow_transaction_update)

                #add transaction to signal movement of the money
                transaction = {
                        "output_wallet_address":escrow_transaction.output_wallet_address.pk,
                        "input_wallet_address":escrow_transaction.input_wallet_address.pk,
                        "transaction_type":escrow_transaction.transaction_type,
                        "transaction_id":str(generate_transaction_id()),
                        "transaction_amount":escrow_transaction.amount_initiated,
                    }

                wallet_transaction = WalletTransactionsSerializer(data=transaction)
                wallet_transaction.is_valid(raise_exception=True)
                wallet_transaction.save()

                #create the certificate and return the link
                certificate.save(certificate_owner=escrow_transaction.output_wallet_address)

                #2 calls are being made to the database, This should be fixed
                certificate_to_update = Certificate.objects.get(pk=certificate.data['id'])

                #create certificate_unique_hash
                unique_string_nonce = generate_transaction_id()
                certificate_unique_hash = generate_certificate_link(escrow_transaction.output_wallet_address, escrow_transaction.input_wallet_address, unique_string_nonce, certificate_to_update.student_number)

                certificate_detail_update = {
                    "unique_string_nonce": str(unique_string_nonce),
                    "certificate_unique_hash":certificate_unique_hash,
                    "verified_by":escrow_transaction.input_wallet_address
                }

                Certificate.objects.update_or_create(
                    id=certificate_to_update.pk, defaults=certificate_detail_update)

                certificate_to_detail = Certificate.objects.get(pk=certificate.data['id'])
                certificate_to_detail_json = CertificateDetailSerializer(certificate_to_detail)

                data_dict = {"status":200, "data":{"certificate_link":certificate_to_detail_json.data, "transaction_details":wallet_transaction.data}}
                return Response(data_dict, status=status.HTTP_200_OK)
            else:
                return Response({"status":400, "error":"Document was already verified"},status=status.HTTP_404_NOT_FOUND)
            # except:
            #     return Response({"status":404, "error":"Document doesnt exist"},status=status.HTTP_404_NOT_FOUND)
        return Response(certificate.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateGrantRequest(APIView):

    permission_classes = (permissions.IsAuthenticated, EmployerPermissions)

    def post(self, request):

        certificate_grant = CertificateGrantAccessSerializer(data=request.data)
        if certificate_grant.is_valid():
            try:
                related_certificate = Certificate.objects.get(certificate_unique_hash=certificate_grant.data['verified_link'])

                #verify provided data.
                print(related_certificate.certificate_owner)
                compare_hash = generate_certificate_link(related_certificate.certificate_owner.wallet_address, related_certificate.verified_by.wallet_address, related_certificate.unique_string_nonce, certificate_grant.data['student_number'])

                # print(compare_hash)
                if compare_hash == certificate_grant.data['verified_link']:

                    #move the money to the institution wallet
                    employer_wallet     = Wallet.objects.get(wallet_address=certificate_grant.data['wallet_address'])

                    institution_wallet   =  Wallet.objects.get(wallet_address=related_certificate.verified_by.wallet_address)

                    employer_wallet_update = {
                        "wallet_balance": float(employer_wallet.wallet_balance)-float(5000),
                    }

                    institution_amount_update = {
                        "wallet_balance": float(institution_wallet.wallet_balance)+float(5000),
                    }

                    Wallet.objects.update_or_create(
                                id=employer_wallet.pk, defaults=employer_wallet_update)

                    Wallet.objects.update_or_create(
                                id=institution_wallet.pk, defaults=institution_amount_update)

                    related_wallet_updated = Wallet.objects.get(wallet_address=certificate_grant.data['wallet_address'])

                    transaction = {
                        "output_wallet_address":employer_wallet.pk,
                        "input_wallet_address":institution_wallet.pk,
                        "transaction_type":'VIEWING',
                        "transaction_id":str(generate_transaction_id()),
                        "transaction_amount":5000,
                    }

                    wallet_transaction = WalletTransactionsSerializer(data=transaction)
                    wallet_transaction.is_valid(raise_exception=True)
                    wallet_transaction.save()

                    certificate_granted_access = CertificateGrantedAccessSerializer(related_certificate)

                    data_dict = {"status":200, "data":{"certificate_view":certificate_granted_access.data, "transaction_details":wallet_transaction.data}}
                    return Response(data_dict, status=status.HTTP_200_OK)

                else:
                    return Response({"status":400, "error":"Link is not owned by the said student"},status=status.HTTP_404_NOT_FOUND)

            except:
                return Response({"status":404, "error":"This link does not exist, Just arrest that man"},status=status.HTTP_404_NOT_FOUND)

            # data_dict = {"status":200, "data":certificate_grant.data}
            # return Response(data_dict, status=status.HTTP_200_OK)
        return Response(certificate_grant.errors, status=status.HTTP_400_BAD_REQUEST)



