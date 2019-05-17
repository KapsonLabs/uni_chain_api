from rest_framework import serializers

from .models import Certificate, CertificateViewRequests, Documents

class DocumentRequestVerificationSerializer(serializers.Serializer):
    """
    A document request verification serializer
    """
    student_address     = serializers.CharField(max_length=255)
    certificate_link    = serializers.FileField()
    public_key          = serializers.CharField(max_length=255)   
    pay_token           = serializers.CharField(max_length=255)

    # def validate_stu

class DocumentVerificationRequestSerializer(serializers.ModelSerializer):
    """
    A document verification request serializer
    """

    class Meta:
        model = CertificateViewRequests
        fields = ("document_id","verifying_entity","requesting_entity","is_document_verification")

