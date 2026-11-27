from rolepermissions.roles import AbstractUserRole  # type: ignore[import-untyped]


class SystemAdmin(AbstractUserRole):
    available_permissions = {  # type: ignore[var-annotated]
        # users
        "add_user": True,
        "change_user": True,
        "delete_user": True,
        "view_user": True,
        # machines
        "add_machine": True,
        "change_machine": True,
        "delete_machine": True,
        "view_machine": True,
        "restore_machine": True,
        "issue_machine_token": True,
        "revoke_machine_token": True,
        "stream_machine": True,
    }


class Admin(AbstractUserRole):
    available_permissions = {}  # type: ignore[var-annotated]


class Operator(AbstractUserRole):
    available_permissions = {}  # type: ignore[var-annotated]
