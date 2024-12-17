from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    """
    Custom permission to check if the user belongs to the 'admin' group.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the 'admin' group
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="admin").exists()


class IsAdministratorGroup(BasePermission):
    """
    Custom permission to check if the user belongs to the 'administrator' group.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='for administrator staff officer').exists()
    
    
class IsLibraryGroup(BasePermission):
    """
    Custom permission to check if the user belongs to the 'Library' group.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='for library staff').exists()
    
    
class IsLibraryOrAdminGroup(BasePermission):
    """
    Custom permission to check if the user belongs to the 'Library' group.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='librariyan_or_admin').exists()
    
class IsStaff(BasePermission):
    """
    Custom permission to check if the user belongs to the 'Staff' group.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='staff').exists()