from django.db import models
from accounts.models import User
from institutions.models import Institution
from wallets.models import Wallet

class Documents(models.Model):
    document_owner              = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='document_owner_wallet')
    document_link               = models.FileField(upload_to='documents/', blank=True, null=True)
    document_hash               = models.CharField(max_length=255, null=True, blank=True)
    uploaded_on                 = models.DateTimeField(auto_now_add=False, blank=True, null=True)

class Certificate(models.Model):
    certificate_owner           = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='certificate_owner_wallet')
    verification_status         = models.BooleanField(default=False)
    verified_by                 = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='certificate_issuer', null=True, blank=True)
    institution_attached        = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institution_attached', null=True, blank=True)
    verified_on                 = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    certificate_link            = models.FileField(upload_to='certificates/', blank=True, null=True)
    certificate_signature_link  = models.FileField(upload_to='certificates/signatures/', blank=True, null=True)
    institution_public_key      = models.CharField(max_length=300, null=True, blank=True)
    uploaded_on                 = models.DateTimeField(auto_now_add=True)

class CertificateViewRequests(models.Model):
    document_id                     = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='certificate_to_be_verified', null=True, blank=True)
    certificate_id                  = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='certificate_to_be_viewed', null=True, blank=True)
    verifying_entity                = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='entity_verifying_request')
    requesting_entity               = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='entity_requesting_verification')
    is_document_verification        = models.BooleanField(default=False)
    is_certificate_view             = models.BooleanField(default=False)
    verification_view_status        = models.BooleanField(default=False)
    date_requested                  = models.DateTimeField(auto_now_add=True)

class CertificateViews(models.Model):
    viewed_certificate          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_viewed')
    viewed_by                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_viewer')
    date_viewed                 = models.DateTimeField(auto_now_add=True)

class CertificateFeesSettings(models.Model):
    created_by                      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='settings_creator')
    certificate_verification_fee    = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    certificate_reverification_fee  = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    certificate_view_access_fee     = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    date_created                    = models.DateTimeField(auto_now_add=True)
