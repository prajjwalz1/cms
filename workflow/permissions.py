from rest_framework import permissions

class CanApproveWorkflow(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff and request.user.has_perm('workflow.approve_workflow') or request.user.is_superuser)
