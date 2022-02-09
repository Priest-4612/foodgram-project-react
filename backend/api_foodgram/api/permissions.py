from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    actions = ['retrieve', 'update', 'partial_update']

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return view.action in self.actions


class OwnerOnly(BasePermission):

    actions = ['retrieve', 'update', 'partial_update']

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.username == request.user
            and view.action in self.actions
        )
