from datetime import datetime  # noqa: TC003
from enum import StrEnum
from typing import Annotated

from django.db.models import Q
from ninja import FilterLookup
from ninja import FilterSchema


class ShowEnum(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ALL = "all"


class DeletedEnum(StrEnum):
    EXCLUDE = "exclude"
    ONLY = "only"
    INCLUDE = "include"


class RoleEnum(StrEnum):
    SYSTEM_ADMIN = "system_admin"
    ADMIN = "admin"
    OPERATOR = "operator"
    ALL = "all"


class UserFilterSchema(FilterSchema):
    show: ShowEnum = ShowEnum.ACTIVE
    deleted: DeletedEnum = DeletedEnum.EXCLUDE
    role: RoleEnum = RoleEnum.ALL
    date_joined_after: Annotated[datetime | None, FilterLookup("date_joined__gte")] = (
        None
    )
    date_joined_before: Annotated[datetime | None, FilterLookup("date_joined__lte")] = (
        None
    )

    def filter_show(self, value: ShowEnum) -> Q:
        if value == ShowEnum.ACTIVE:
            return Q(is_active=True)
        if value == ShowEnum.INACTIVE:
            return Q(is_active=False)
        return Q()  # all

    def filter_deleted(self, value: DeletedEnum) -> Q:
        if value == DeletedEnum.EXCLUDE:
            return Q(deleted_at__isnull=True)
        if value == DeletedEnum.ONLY:
            return Q(deleted_at__isnull=False)
        return Q()  # include

    def filter_role(self, value: RoleEnum) -> Q:
        if value == RoleEnum.SYSTEM_ADMIN:
            return Q(groups__name="system_admin")
        if value == RoleEnum.ADMIN:
            return Q(groups__name="admin")
        if value == RoleEnum.OPERATOR:
            return Q(groups__name="operator")
        return Q()  # all
