from rest_framework import serializers

from .models import Certificate, CertificateViews, CertificateVerificationRequests

class CertificatesSerializer(serializers.ModelSerializer):
    """
    A serializer that allows certificate uploads
    """
    class Meta:
        model = Certificate
        fields = ('id','student_number','certificate_link', )

class CertificateVerificationRequestSerializer(serializers.ModelSerializer):
    """
    A serializer that receives certificate verification requests
    """
    class Meta:
        model = CertificateVerificationRequests
        fields = ('id','institution_id', 'certificate_id')