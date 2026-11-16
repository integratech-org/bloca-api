from ninja_extra import permissions
from rolepermissions.checkers import has_object_permission
from rolepermissions.checkers import has_permission
from rolepermissions.checkers import has_role


class HasRole(permissions.BasePermission):
    def __init__(self, *roles):
        self.roles = roles

    def has_permission(self, request, controller):
        return bool(request.user and has_role(request.user, list(self.roles)))


class HasPermission(permissions.BasePermission):
    def __init__(self, permission_name):
        self.permission_name = permission_name

    def has_permission(self, request, controller):
        return bool(request.user and has_permission(request.user, self.permission_name))


class HasObjectPermission(permissions.BasePermission):
    def __init__(self, checker_name):
        self.checker_name = checker_name

    def has_permission(self, request, controller):
        return request.user.is_authenticated

    def has_object_permission(self, request, controller, obj):
        return has_object_permission(self.checker_name, request.user, obj)
