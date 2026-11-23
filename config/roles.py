from rolepermissions.roles import AbstractUserRole  # type: ignore[import-untyped]


class SystemAdmin(AbstractUserRole):
    available_permissions = {  # type: ignore[var-annotated]
        "add_user": True,
        "change_user": True,
        "delete_user": True,
        "view_user": True,
    }


class Admin(AbstractUserRole):
    available_permissions = {}  # type: ignore[var-annotated]


class Operator(AbstractUserRole):
    available_permissions = {}  # type: ignore[var-annotated]
