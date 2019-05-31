from django.contrib import admin
from .models import CertificateFeesSettings, Documents, CertificateViewRequests, Certificate

admin.site.register(CertificateFeesSettings)
admin.site.register(Documents)
admin.site.register(CertificateViewRequests)
admin.site.register(Certificate)
