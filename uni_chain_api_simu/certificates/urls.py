from django.urls import path, include
from .views import RequestCertificateVerification, VerificationRequests, VerifiedCertificateUpload, CertificateGrantRequest

urlpatterns = [
    path('certificates/request_verification/', RequestCertificateVerification.as_view(), name="request_certificate_verification"),
    path('institutions/verification_requests/', VerificationRequests.as_view(), name="institution_verification_requests"),
    path('institutions/certificates/upload/', VerifiedCertificateUpload.as_view(), name="institution_certificate_upload"),
    path('certificates/request_access/', CertificateGrantRequest.as_view(), name="certificate_request_access"),
]