from datetime import datetime  # noqa: TC003
from enum import StrEnum
from typing import Annotated

from django.db.models import Q
from ninja import FilterLookup
from ninja import FilterSchema

from .models import Machine


class DeletedEnum(StrEnum):
    EXCLUDE = "exclude"
    ONLY = "only"
    INCLUDE = "include"


class MachineFilterSchema(FilterSchema):
    deleted: DeletedEnum = DeletedEnum.EXCLUDE
    token_status: Machine.TokenStatus | None = Machine.TokenStatus.ACTIVE
    created_after: Annotated[datetime | None, FilterLookup("created_at__gte")] = None
    created_before: Annotated[datetime | None, FilterLookup("created_at__lte")] = None

    def filter_deleted(self, value: DeletedEnum) -> Q:
        if value == DeletedEnum.EXCLUDE:
            return Q(deleted_at__isnull=True)
        if value == DeletedEnum.ONLY:
            return Q(deleted_at__isnull=False)
        return Q()  # include

    def filter_token_status(self, value: Machine.TokenStatus | None) -> Q:
        if value == Machine.TokenStatus.ACTIVE:
            return Q(revoked_at__isnull=True, token_hash__isnull=False)
        if value == Machine.TokenStatus.REVOKED:
            return Q(revoked_at__isnull=False)
        if value == Machine.TokenStatus.NOT_ISSUED:
            return Q(revoked_at__isnull=True, token_hash__isnull=True)
        return Q()
