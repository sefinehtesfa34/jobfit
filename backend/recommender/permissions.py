from rest_framework import permissions 
class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        super().has_object_permission(request, view, obj)
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.userId == obj.userId
    