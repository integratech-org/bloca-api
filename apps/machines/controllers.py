from uuid import UUID  # noqa: TC003

from allauth.headless.contrib.ninja.security import x_session_token_auth
from django.http import StreamingHttpResponse
from django.shortcuts import aget_object_or_404
from injector import inject
from ninja import Query  # noqa: TC002
from ninja.responses import Status
from ninja.security import django_auth
from ninja_extra import api_controller
from ninja_extra import paginate
from ninja_extra import route
from ninja_extra.ordering import Ordering
from ninja_extra.ordering import ordering
from ninja_extra.pagination import PageNumberPaginationExtra
from ninja_extra.pagination import PaginatedResponseSchema
from ninja_extra.searching import Searching
from ninja_extra.searching import searching

from config.permissions import HasPermission

from .filters import MachineFilterSchema  # noqa: TC001
from .models import Machine
from .schemas import MachineCreateIn
from .schemas import MachineCreateOut
from .schemas import MachineIssueTokenOut
from .schemas import MachineOut
from .schemas import MachineUpdateIn
from .schemas import MachineUpdateOut
from .services import MachineService  # noqa: TC001


@api_controller(
    "/machines",
    tags=["Machines"],
    auth=[x_session_token_auth, django_auth],
)
class MachineController:
    @inject
    def __init__(self, machines_service: MachineService):
        self.machines_service = machines_service

    @route.get(
        "/",
        response=PaginatedResponseSchema[MachineOut],
        permissions=[HasPermission("view_machine")],
    )
    @paginate(PageNumberPaginationExtra, page_size=25)
    @ordering(
        Ordering,
        ordering_fields=["name", "created_at"],
    )
    @searching(Searching, search_fields=["name", "site"])
    def get_machines(self, filters: Query[MachineFilterSchema]):
        return self.machines_service.list_machines(filters)

    @route.post(
        "/",
        response={201: MachineCreateOut},
        permissions=[HasPermission("add_machine")],
    )
    def create_machine(self, payload: MachineCreateIn):
        return Status(201, self.machines_service.create_machine(payload))

    @route.get(
        "/{machine_id}/",
        response={200: MachineOut},
        permissions=[HasPermission("view_machine")],
    )
    def get_machine(self, machine_id: UUID):
        return self.machines_service.get_machine(machine_id)

    @route.patch(
        "/{machine_id}/",
        response={200: MachineUpdateOut},
        permissions=[HasPermission("change_machine")],
    )
    def update_machine(self, machine_id: UUID, payload: MachineUpdateIn):
        return Status(200, self.machines_service.update_machine(machine_id, payload))

    @route.delete(
        "/{machine_id}/",
        response={204: None},
        permissions=[HasPermission("delete_machine")],
    )
    def delete_machine(self, machine_id: UUID):
        self.machines_service.delete_machine(machine_id)
        return Status(204, None)

    @route.post(
        "/{machine_id}/restore/",
        response={204: None},
        permissions=[HasPermission("restore_machine")],
    )
    def restore_machine(self, machine_id: UUID):
        self.machines_service.restore_machine(machine_id)
        return Status(204, None)

    @route.post(
        "/{machine_id}/token/",
        response={200: MachineIssueTokenOut},
        permissions=[HasPermission("issue_machine_token")],
    )
    def issue_token(self, machine_id: UUID):
        return Status(200, self.machines_service.issue_token(machine_id))

    @route.post(
        "/{machine_id}/token/revoke/",
        response={204: None},
        permissions=[HasPermission("revoke_machine_token")],
    )
    def revoke_token(self, machine_id: UUID):
        self.machines_service.revoke_token(machine_id)
        return Status(204, None)

    @route.get("/{machine_id}/stream/", permissions=[HasPermission("stream_machine")])
    async def stream(self, machine_id: UUID):
        machine = await aget_object_or_404(Machine, id=machine_id)
        res = StreamingHttpResponse(
            self.machines_service.stream_events(machine.id),
            content_type="text/event-stream",
        )
        res["Cache-Control"] = "no-cache"
        res["X-Accel-Buffering"] = "no"
        return res
