from rest_framework.permissions import BasePermission
from .models import User

class InstitutionAdministratorPermissions(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_institution and request.user.is_active

class StudentPermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_student and request.user.is_active

class EmployerPermissions(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_employer and request.user.is_active