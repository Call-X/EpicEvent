from rest_framework import permissions
from core.models import CustomUser
from client.models import CustomClient
from contracts.models import Contract, Event
from rest_framework.exceptions import PermissionDenied

""" Managers have the permission to read_only on the crm;
the other method like Post, Retrieve, Delete, Update have 
to be done throught the admin site
"""

class IsManager(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     return request.user.usergroup == CustomUser.UserGroupe.MANAGEMENT and request.method in permissions.SAFE_METHODS
    
    # def has_object_permission(self, request, view, obj):
    #     return request.user.usergroup == CustomUser.UserGroupe.MANAGEMENT and request.method in permissions.SAFE_METHODS
    
    def has_object_permission(self, request):
        # Read permissions are allowed to project contributors
        if request.method in permissions.SAFE_METHODS:
            return CustomUser.objects.filter(is_admin=request.user).exists()
            

        # Delete is only allowed to project manager if there is at least 2
        # contract managers registered for the project
        elif request.method == 'DELETE':
            return CustomUser.objects.filter(is_admin=request.user, usergroup=CustomUser.UserGroupe.MANAGEMENT).exists() 
            
        # Create is only allowed to project manager
        elif request.method == 'POST':
            return CustomUser.objects.filter(
                    is_admin=request.user, usergroup=CustomUser.UserGroupe.MANAGEMENT
                    ).exists()
        else:
            return False
    
class ClientPermissions(permissions.BasePermission):
    
    """Sale team : can CREATE new clients or/and prospects
                    can VIEW and UPDATE any prospect and their own clients
                    can DELETE just the prospect
        Support team : can VIEW clients of their own contracts
    """
    # def has_permission(self, request, view):
    #     if request.user.usergroup in (CustomUser.UserGroupe.MANAGEMENT, CustomUser.UserGroupe.SUPPORT):
    #         return request.method in permissions.SAFE_METHODS
    #     return request.user.usergroup == CustomUser.UserGroupe.SALE
    
    # def has_object_permission(self, request, view, obj):
    #     if request.user.usergroup == CustomUser.UserGroupe.SALE:
    #         if request.method == 'DELETE':
    #             return request.user.usergroup == CustomUser.UserGroupe.SALE and obj.is_prospect
    #         else:
    #             return obj.sales_contact == request.user or obj.is_prospect
    #     elif request.user.usergroup == CustomUser.UserGroupe.SUPPORT:
    #         return request.method in permissions.SAFE_METHODS
    
 
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to project contributors
        if request.method in permissions.SAFE_METHODS:
            return CustomUser.objects.filter(
                    is_admin=request.user, usergroupe=CustomUser.UserGroupe.SALE).exists()

        # Delete is only allowed to project manager if there is at least 2
        # contract managers registered for the project
        if request.method == 'DELETE':
            return CustomUser.objects.filter(
                is_admin=request.user,
                usergroup=CustomUser.CustomUser.UserGroupe.SALE and obj.is_prospect).exists() 
        if not request.method == 'DELETE': 
            return obj.sales_contact == request.user or obj.is_prospect
            
        # Create is only allowed to project manager
        elif request.method == 'POST':
            return CustomUser.objects.filter(
                    is_admin=request.user, usergroup=CustomUser.UserGroupe.SUPPORT
                    ).exists()
        else:
            return False
    
class ContractPermissions(permissions.BasePermission):
    
    """Sales team : can CREATE new contracts
                    can VIEW contracts and UPDATE contracts of their clients until the contract is conclued
        Support team : can VIEW their clients contracts
    """
    # def  has_permission(self, request, view):
    #     print("coucou")
    #     if request.user == CustomUser.UserGroupe.SUPPORT:
    #         print("coucou2")
    #         return request.method in permissions.SAFE_METHODS
    #     return request.user == CustomUser.UserGroupe.SALE
    
    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         # if request.user.usergroup == UserModel.UserGroup.SUPPORT:
    #         #     return obj in Contract.objects.filter(
    #         #         event__support_contact=request.user
    #         #     )
    #         return request.user == obj.sales_contact or request.user == obj.event__support_sales_contact
    #     elif request.method == "PUT" and obj.status == "OPEN":
    #         return request.user.usergroup == CustomUser.UserGroupe.SALE
    #     else:
    #         raise PermissionDenied("Cannot update a signed contract.")
    
    def has_object_permission(self, request, view, obj):
        print("coucou3")
        # Read permissions are allowed to project contributors
        if request.method in permissions.SAFE_METHODS:
            print("coucou4")
            if CustomUser.objects.filter(is_admin=request.user, usergroup=CustomUser.UserGroupe.SALE).exists():
                print("coucou5")
                return obj in Contract.objects.filter(event__support_contact=request.user)
            return request.user == obj.sales_contact or request.user == obj.event__support_sales_contact
                
        elif request.method == "PUT" and obj.status == "OPEN":
            print("coucou6")
            return CustomUser.objects.filter(is_admin=request.user, usergroup=CustomUser.UserGroupe.SALE).exists()
        else:
            print("coucou7")
            raise PermissionDenied("Cannot update a signed contract.")
        
        
class EventPermissions(permissions.BasePermission):
    
    """ Sales team : can CREATE new events
                     can VIEW events of their own clients
                     can UPDATE events of their own clients if not finished
        Support team : can VIEW events of their own clients
                       can UPDATE events of their own clients if not finished
    """

    # def has_permission(self, request, view):
    #     request_method = request.method

    #     if request.user == CustomUser.UserGroup.MANAGEMENT:
    #         return request_method in permissions.SAFE_METHODS

    #     if request.user in (CustomUser.UserGroup.SUPPORT):
    #         return request_method not in ("DELETE", "CREATE")

    #     return request_method != "DELETE"

    # def has_object_permission(self, request, view, obj):
    #     request_method = request.method

    #     if request_method in permissions.SAFE_METHODS:
    #         return request.user in (obj.contract.sales_contact, obj.support_contact)
    #     if request_method in ("PUT","CREATE"):
    #         return request.user in (obj.contract.sales_contact, obj.support_contact)
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to project contributors
        if request.method in permissions.SAFE_METHODS:
            return CustomUser.objects.filter(
                    is_admin=request.user, usergroup=CustomUser.UserGroupe.SALE).exists()

        # Delete is only allowed to project manager if there is at least 2
        # contract managers registered for the project
        
        if CustomUser.objects.filter(
                is_admin=request.user,
                usergroup=CustomUser.UserGroupe.SALE and obj.is_prospect).exists():
            return request.method == ['GET', 'PUT']
            
        # Create is only allowed to project manager
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.support_contact or request.user == obj.contract.sales_contact
        else:
            if obj.event_status is True:
                raise PermissionDenied("Cannot update a finished event.")
            if CustomUser.objects.filter(
                    is_admin=request.user, usergroup=CustomUser.UserGroupe.SALE).exists():
                return request.user == obj.support_contact
            return request.user == obj.contract.sales_contact
            
    
    