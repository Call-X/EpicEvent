from rest_framework import permissions
from core.models import CustomUser
from rest_framework.exceptions import PermissionDenied

""" Managers have the permission to read_only on the crm;
the other method like Post, Retrieve, Delete, Update have 
to be done throught the admin site
"""

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.usergroup == CustomUser.UserGroupe.MANAGEMENT and request.method in permissions.SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return request.user.usergroup == CustomUser.UserGroupe.MANAGEMENT and request.method in permissions.SAFE_METHODS
    
class ClientPermissions(permissions.BasePermission):
    
    """Sale team : can CREATE new clients or/and prospects
                    can VIEW and UPDATE any prospect and their own clients
                    can DELETE just the prospect
        Support team : can VIEW clients of their own contracts
    """
    def has_permission(self, request, view):
        if request.user.usergroup in (CustomUser.UserGroupe.MANAGEMENT, CustomUser.UserGroupe.SUPPORT):
            return request.method in permissions.SAFE_METHODS
        return request.user.usergroupe == CustomUser.UserGroupe.SALE
    
    def has_object_permission(self, request, view, obj):
        if request.user.usergroupe == CustomUser.UserGroupe.SALE:
            if request.method == 'DELETE':
                return request.user.usergroup == CustomUser.UserGroupe.SALE and obj.is_prospect
            else:
                return obj.sales_contact == request.user or obj.is_prospect
        elif request.user.usergroup == CustomUser.UserGroupe.SUPPORT:
            return request.method in permissions.SAFE_METHODS
        
class ContractPermissions(permissions.BasePermission):
    
    """Sales team : can CREATE new contracts
                    can VIEW contracts and UPDATE contracts of their clients until the contract is conclued
        Support team : can VIEW their clients contracts
    """
    def  has_permission(self, request, view):
        if request.user.usergroup == CustomUser.UserGroupe.SUPPORT:
            return request.method in permissions.SAFE_METHODS
        return request.user.usergroup == CustomUser.UserGroupe.SALE
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # if request.user.usergroup == UserModel.UserGroup.SUPPORT:
            #     return obj in Contract.objects.filter(
            #         event__support_contact=request.user
            #     )
            return request.user == obj.sales_contact or request.user == obj.event__support_sales_contact
        elif request.method == "PUT" and obj.status == "OPEN":
            return request.user.usergroup == CustomUser.UserGroup.SALE
        else:
            raise PermissionDenied("Cannot update a signed contract.")
        
        
class EventPermissions(permissions.BasePermission):
    
    """ Sales team : can CREATE new events
                     can VIEW events of their own clients
                     can UPDATE events of their own clients if not finished
        Support team : can VIEW events of their own clients
                       can UPDATE events of their own clients if not finished
    """

    def has_permission(self, request, view):
        request_method = request.method

        if request.user.usergroup == CustomUser.UserGroup.MANAGEMENT:
            return request_method in permissions.SAFE_METHODS

        if request.user.usergroup in (CustomUser.UserGroup.SUPPORT):
            return request_method not in ("DELETE", "CREATE")

        return request_method != "DELETE"

    def has_object_permission(self, request, view, obj):
        request_method = request.method

        if request_method in permissions.SAFE_METHODS:
            return request.user in (obj.contract.sales_contact, obj.support_contact)
        if request_method in ("PUT","CREATE"):
            return request.user in (obj.contract.sales_contact, obj.support_contact)
    
    