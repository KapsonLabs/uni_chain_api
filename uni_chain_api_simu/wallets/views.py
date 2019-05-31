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

from accounts.permissions import StudentPermissions, EmployerPermissions, InstitutionEmployerStudentPermissions, InstitutionAdministratorPermissions
from .models import Wallet, WalletTransactions, EscrowTransactions
from certificates.models import CertificateFeesSettings
from certificates.serializers import AddressSerializer
from .serializers import WalletNumberSerializer, WalletTransactionsSerializer, WalletDetailsSeriliazer, PayTokensSerializer, WalletTransactionsDetailSerializer, PayTokenAddressSerializer, PayTokensDetailSerializer, WalletBalanceSerializer, WalletTransactionsHistorySerialiazer, EscrowTransactionsSerializer, PredictSerializer

from .helpers import generate_pay_id, generate_transaction_id

###damalie's project###
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

 
import urllib.request
import json

class WalletTopUp(generics.CreateAPIView):
    """
    Withdraw savings from account
    """
    permission_classes = (permissions.IsAuthenticated, InstitutionEmployerStudentPermissions, )

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
                    "transaction_id":str(generate_transaction_id()),
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
                    "transaction_id":wallet_transaction.data['transaction_id'],
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
            
            pay_id         = generate_pay_id(transaction_id, addresses.data['institution_wallet_address'], student_wallet.wallet_public_key)

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


class WalletBalance(APIView):
    permission_classes = (permissions.IsAuthenticated, InstitutionEmployerStudentPermissions)

    def post(self, request):
        address = AddressSerializer(data=request.data)
        if address.is_valid():
            try:
                account_balance = Wallet.objects.get(wallet_address=address.data['wallet_address'])

                balance_serializer = WalletBalanceSerializer(account_balance)

                data_dict = {"status":200, "data":balance_serializer.data}
                return Response(data_dict, status=status.HTTP_200_OK)
            except:
                data_dict = {"status":404, "error":"wallet address doesnot exist"}
                return Response(data_dict, status=status.HTTP_404_NOT_FOUND)
        return Response(address.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletTransactionHistory(APIView):
    permission_classes = (permissions.IsAuthenticated, InstitutionEmployerStudentPermissions)

    def post(self, request):
        address = AddressSerializer(data=request.data)
        if address.is_valid():
            try:
                wallet = Wallet.objects.get(wallet_address=address.data['wallet_address'])

                wallet_transactions = WalletTransactions.objects.filter(input_wallet_address=wallet)

                wallet_transaction_serializer = WalletTransactionsHistorySerialiazer(wallet_transactions, many=True)

                data_dict = {"status":200, "data":wallet_transaction_serializer.data}
                return Response(data_dict, status=status.HTTP_200_OK)
            except:
                data_dict = {"status":404, "error":"wallet address doesnot exist"}
                return Response(data_dict, status=status.HTTP_404_NOT_FOUND)
        return Response(wallet_transactions.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletEscrowTransactions(APIView):
    permission_classes = (permissions.IsAuthenticated, InstitutionAdministratorPermissions)

    def post(self, request):
        address = AddressSerializer(data=request.data)
        if address.is_valid():
            try:
                wallet = Wallet.objects.get(wallet_address=address.data['wallet_address'])

                wallet_escrow_transactions = EscrowTransactions.objects.filter(input_wallet_address=wallet)

                escrow_transaction_serializer = EscrowTransactionsSerializer(wallet_escrow_transactions, many=True)

                data_dict = {"status":200, "data":escrow_transaction_serializer.data}
                return Response(data_dict, status=status.HTTP_200_OK)
            except:
                data_dict = {"status":404, "error":"wallet address doesnot exist"}
                return Response(data_dict, status=status.HTTP_404_NOT_FOUND)
        return Response(escrow_transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#### DAMALIE'S PROJECT #####
class PredictData(APIView):

    def post(self, request):
        predict_data = PredictSerializer(data=request.data)
        if predict_data.is_valid():
            
            data_list = [[float(predict_data.data['employee'])], [float(predict_data.data['ownership'])], [float(predict_data.data['credit_history'])], [float(predict_data.data['sales'])], [float(predict_data.data['credit'])], [float(predict_data.data['turnover'])], [float(predict_data.data['age_of_business'])], [float(predict_data.data['fixed_asset_value'])], [float(predict_data.data['defaulted'])], [float(predict_data.data['business_type'])]]

            #code from damalie's script
            scaler=MinMaxScaler()
            X_scaled = scaler.fit(data_list).transform(data_list)
            # data_pred=pd.DataFrame(X_scaled)

            data = {
            "Inputs": {
                "input1":
                    [
                        {
                            'employees': str(X_scaled[0][0]),   
                            'ownership': str(X_scaled[1][0]),   
                            'credithistory': str(X_scaled[2][0]),   
                            'sales': str(X_scaled[3][0]),   
                            'credit': str(X_scaled[4][0]),   
                            'turnover': str(X_scaled[5][0]),   
                            'ageOfBusiness': str(X_scaled[6][0]),   
                            'fixedAssetValue': str(X_scaled[7][0]),   
                            'TypeOfSme': str(X_scaled[8][0]),   
                            'buzType': str(X_scaled[9][0]),   
                        }
                    ],
                },
            "GlobalParameters":  {
                }
            }

            body = str.encode(json.dumps(data))

            url = 'https://ussouthcentral.services.azureml.net/workspaces/50da1d9cd1e5469eab09313ce2d8a5c4/services/4552f90f56554d82a3faa599d5210fc9/execute?api-version=2.0&format=swagger'
            api_key = 'sTZ/aMyKXz9U0Xw4I66/xP9KRmHhT1IqH2uK8UZXunxxeEyrkTJBaKBxOs46R4/fluhx7jn+ZkovUtEGOUftPQ==' # Replace this with the API key for the web service
            headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

            req = urllib.request.Request(url, body, headers)

            try:
                response = urllib.request.urlopen(req)

                result = response.read()
                #decode result from binary string to dictionary
                decoded_result=json.loads(result.decode())

                scored_label = decoded_result['Results']['output1'][0]['Scored Label Mean']
                print(scored_label)
            except urllib.error.HTTPError as error:
                print("The request failed with status code: " + str(error.code))

                # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
                print(error.info())
                print(json.loads(error.read().decode("utf8", 'ignore')))

            return Response({"data":{"scored_label":scored_label, "status":200}},status=status.HTTP_200_OK)
        return Response(predict_data.errors, status=status.HTTP_400_BAD_REQUEST)




