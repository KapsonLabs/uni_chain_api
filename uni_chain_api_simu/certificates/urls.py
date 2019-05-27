from django.urls import path, include
from .views import RequestCertificateVerification, VerificationRequests, VerifiedCertificateUpload

urlpatterns = [
    path('certificates/request_verification/', RequestCertificateVerification.as_view(), name="request_certificate_verification"),
    path('institutions/verification_requests/', VerificationRequests.as_view(), name="institution_verification_requests"),
    path('institutions/certificates/upload/', VerifiedCertificateUpload.as_view(), name="institution_certificate_upload"),
]