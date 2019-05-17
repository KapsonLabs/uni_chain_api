from django.urls import path, include
from .views import RequestCertificateVerification

urlpatterns = [
    path('certificates/request_verification/', RequestCertificateVerification.as_view(), name="request_certificate_verification"),
]