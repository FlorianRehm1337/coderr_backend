from rest_framework import permissions

class IsBusinessAccount(permissions.BasePermission):

    def has_permission(self, request, view):

        if hasattr(request.user, 'business'):
            return True

class IsOfferCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user == obj.user:
            return True
