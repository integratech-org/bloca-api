from typing import ClassVar

from rolepermissions.roles import AbstractUserRole  # type: ignore[import-untyped]


class SystemAdmin(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {
        "add_user": True,
        "change_user": True,
        "delete_user": True,
        "view_user": True,
    }


class Admin(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {}


class Operator(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {}
