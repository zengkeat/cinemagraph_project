from rest_framework.permissions import BasePermission

# create our own permission for only object owner can overide their object
# https://www.youtube.com/watch?v=-0c88d24qzM&index=11&list=PLEsfXFp6DpzTOcOVdZF-th7BS_GYGguAS
class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
