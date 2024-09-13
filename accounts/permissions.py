from rest_framework import permissions
from .models import UserInvestmentAccount

class InvestmentAccountPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # General permission check: allow authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object-level permission: `obj` is the InvestmentAccount instance
        try:
            user_investment_account = UserInvestmentAccount.objects.get(user=request.user, investment_account=obj)

            # Check permissions based on HTTP methods
            if request.method == 'GET' and user_investment_account.permission_level == UserInvestmentAccount.VIEW_ONLY:
                return True  # Allow view-only access

            if request.method in ['GET', 'POST' ,'PUT', 'PATCH', 'DELETE'] and user_investment_account.permission_level == UserInvestmentAccount.FULL_CRUD:
                return True  # Allow full CRUD operations

            if request.method == 'POST' and user_investment_account.permission_level == UserInvestmentAccount.POST_ONLY:
                return True  # Allow only creating transactions

            # If no conditions are met, deny access
            return False
        except UserInvestmentAccount.DoesNotExist:
            return False  # Deny access if the user is not linked to the investment account
