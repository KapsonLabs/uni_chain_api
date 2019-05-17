from django.db import models
from accounts.models import User

class Institution(models.Model):
    institution_name            = models.CharField(max_length=100)
    created_by                  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True ,related_name='institution_creator')
    created_on                  = models.DateTimeField(auto_now_add=True)