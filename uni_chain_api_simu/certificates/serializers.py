from rest_framework import serializers

from .models import Certificate, CertificateViewRequests, Documents
from wallets.models import PayTokens

class DocumentRequestVerificationSerializer(serializers.Serializer):
    """
    A document request verification serializer
    """
    student_address     = serializers.CharField(max_length=255)
    certificate_link    = serializers.FileField(max_length=None, allow_empty_file=False)
    public_key          = serializers.CharField(max_length=255)   
    pay_token           = serializers.CharField(max_length=255)

    # def validate_pay_token(self, value):
    #     token = PayTokens.objects.get(token_issued=self.initial_data['pay_token'])
    #     value = token
    #     if value.token_active==True:
    #         raise serializers.ValidationError("This token has already been used, Please request another one")
    #     return value

class DocumentUploadSerializer(serializers.ModelSerializer):
    """
    A document upload serializer
    """

    class Meta:
        model = Documents
        fields = ("id","document_link")

# class DocumentVerificationRequestSerializer(serializers.ModelSerializer):
#     """
#     A document verification request serializer
#     """

#     document_id         = DocumentUploadSerializer(read_only=True)
#     # verifying_entity    = WalletAddressSerializer(read_only=True)
#     # requesting_entity   = WalletAddressSerializer(read_only=True)

#     class Meta:
#         model = CertificateViewRequests
#         fields = ("id", "document_id","verifying_entity","requesting_entity")

class AddressSerializer(serializers.Serializer):
    wallet_address     = serializers.CharField(max_length=255)

class CertificateUploadSerializer(serializers.ModelSerializer):
    """
    Cerificate upload serializer
    """

    class Meta:
        model = Certificate
        fields = ('certificate_link', 'student_name', 'student_number')

