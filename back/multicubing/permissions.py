from rest_framework.permissions import BasePermission


def AuthenticatedExceptActions(actions):
    class _AuthenticatedExceptActions(BasePermission):
        def has_permission(self, request, view):
            if not request.user.is_authenticated:
                if view.action in actions:
                    return True
                else:
                    return False
            else:
                return True
    return _AuthenticatedExceptActions
