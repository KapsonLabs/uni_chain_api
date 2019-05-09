from django.db import models
from accounts.models import User

class Institution(models.Model):
    institution_name            = models.CharField(max_length=100)
    institution_public_key      = models.CharField(max_length=300, null=True, blank=True)
    created_on                  = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    certificate_owner           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_owner_student')
    verification_status         = models.BooleanField(default=False)
    verified_by                 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_issuer', null=True, blank=True)
    institution_attached        = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institution_attached', null=True, blank=True)
    verified_on                 = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    student_number              = models.CharField(max_length=100)
    certificate_link            = models.FileField(upload_to='certificates/', blank=True, null=True)
    institution_public_key      = models.CharField(max_length=300, null=True, blank=True)
    uploaded_on                 = models.DateTimeField(auto_now_add=True)

class CertificateVerificationRequests(models.Model):
    certificate_id              = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='certificate_to_be_verified')
    institution_id              = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institution_to_verify')
    requested_by                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_by')
    verification_status         = models.BooleanField(default=False)
    date_requested              = models.DateTimeField(auto_now_add=True)

class CertificateViews(models.Model):
    viewed_certificate          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_viewed')
    viewed_by                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificate_viewer')
    date_viewed                 = models.DateTimeField(auto_now_add=True)