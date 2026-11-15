from uuid import UUID  # noqa: TC003

from django.http import StreamingHttpResponse
from django.shortcuts import aget_object_or_404
from injector import inject
from ninja.responses import Status
from ninja_extra import api_controller
from ninja_extra import paginate
from ninja_extra import route
from ninja_extra.ordering import Ordering
from ninja_extra.ordering import ordering
from ninja_extra.pagination import PageNumberPaginationExtra
from ninja_extra.pagination import PaginatedResponseSchema

from apps.machines.models import Machine

from .schemas import MachineCreateIn
from .schemas import MachineCreateOut
from .schemas import MachineIssueTokenOut
from .schemas import MachineOut
from .schemas import MachineUpdateIn
from .schemas import MachineUpdateOut
from .services import MachineService  # noqa: TC001


@api_controller("/machines", tags=["Machines"])
class MachineController:
    @inject
    def __init__(self, machines_service: MachineService):
        self.machines_service = machines_service

    @route.get("/", response=PaginatedResponseSchema[MachineOut])
    @paginate(PageNumberPaginationExtra, page_size=25)
    @ordering(
        Ordering,
        ordering_fields=["created_at"],
    )
    def get_machines(self):
        return self.machines_service.list_machines()

    @route.post("/", response={201: MachineCreateOut})
    def create_machine(self, payload: MachineCreateIn):
        return Status(201, self.machines_service.create_machine(payload))

    @route.get("{machine_id}/", response={200: MachineOut})
    def get_machine(self, machine_id: UUID):
        return self.machines_service.get_machine(machine_id)

    @route.patch("{machine_id}/", response={200: MachineUpdateOut})
    def update_machine(self, machine_id: UUID, payload: MachineUpdateIn):
        return Status(200, self.machines_service.update_machine(machine_id, payload))

    @route.delete("{machine_id}/", response={204: None})
    def delete_machine(self, machine_id: UUID):
        self.machines_service.delete_machine(machine_id)
        return Status(204, None)

    @route.post("{machine_id}/token/", response={200: MachineIssueTokenOut})
    def issue_token(self, machine_id: UUID):
        return Status(200, {"token": self.machines_service.issue_token(machine_id)})

    @route.post("{machine_id}/token/revoke/", response={204: None})
    def revoke_token(self, machine_id: UUID):
        self.machines_service.revoke_token(machine_id)
        return Status(204, None)

    @route.get("{machine_id}/stream")
    async def stream(self, machine_id: UUID):
        machine = await aget_object_or_404(Machine, id=machine_id)
        res = StreamingHttpResponse(
            self.machines_service.stream_events(machine.id),
            content_type="text/event-stream",
        )
        res["Cache-Control"] = "no-cache"
        res["X-Accel-Buffering"] = "no"
        return res
