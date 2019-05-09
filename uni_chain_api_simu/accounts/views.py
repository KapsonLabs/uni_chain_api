from accounts.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from accounts.serializers import TokenSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .serializers import CreateUserSerializer
from wallets.helpers import generate_account_number
from wallets.serializers import WalletsSerializer

#
"""
Everything inside here is heavily dangerous
Touch nothing

#########################
WRITTEN BY THE DANGEROUS 
SMOKING HEAD OF MR.
ALLAN KATONGOLE
#########################
##############################################
"""
#####################################################
from subprocess import Popen, PIPE, STDOUT
####################################################
"""
Dangerous minefield
Stay away
#############################################
"""

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            token_serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            token_serializer.is_valid()
            return Response(token_serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RegisterView(generics.CreateAPIView):
    """
    POST auth/register/
    """

    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    def post(self,request, *args, **kwargs):
        user_data = request.data.copy()
        role    = user_data.pop('role', None)

        serializer = CreateUserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save(is_student=True)

            user = User.objects.get(pk=serializer.data['id'])

            """
            ####################################################################
            DO NOT TOUCH...... INFACT STAY AWAY
            ####################################################################
            """

            command = ["bash","/Users/allan-only/projects/blockchain/uni-chain-api/uni_chain_api_simu/sorcery_scripts/bin/hello_sorcery.sh"]
            try:
                    process = Popen(command, stdout=PIPE, stderr=STDOUT)
                    output = process.stdout.read()
                    exitstatus = process.poll()
                    if (exitstatus==0):
                            result = {"status": "Success", "output":output}
                    else:
                            result = {"status": "Failed", "output":output}

            except Exception as e:
                    result =  {"status": "failed", "output":str(e)}

            print(result['output'].decode()[9:])

            """
            ###################################################################
            THANK YOU FOR NOT TOUCHING, HAVE A GOOD CODING DAY.
            ###################################################################
            """
            wallet_number = generate_account_number(serializer.data['id'])

            user_wallet = {
                "wallet_number":wallet_number,
                "wallet_address":result['output'].decode()[9:],
                "wallet_private_key":result['output'].decode()[9:],
                "wallet_public_key":result['output'].decode()[9:],
            }

            wallet_creation = WalletsSerializer(data=user_wallet)
            wallet_creation.is_valid(raise_exception=True)
            wallet_creation.save(wallet_owner=user)

            data_dict = {"status":201, "data":serializer.data, "wallet_info":wallet_creation.data}
            return Response(data_dict, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)