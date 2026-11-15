from uuid import UUID  # noqa: TC003

from django.http import StreamingHttpResponse
from django.shortcuts import aget_object_or_404
from injector import inject
from ninja.responses import Status
from ninja_extra import api_controller
from ninja_extra import route

from apps.machines.models import Machine

from .schemas import MachinesCreateIn
from .schemas import MachinesCreateOut
from .services import MachinesService  # noqa: TC001


@api_controller("/machines", tags=["Machines"])
class MachinesController:
    @inject
    def __init__(self, machines_service: MachinesService):
        self.machines_service = machines_service

    @route.get("/")
    def get_machines(self):
        return {"message": "List of machines"}

    @route.post("/", response={201: MachinesCreateOut})
    def create_machine(self, payload: MachinesCreateIn):
        return Status(201, self.machines_service.create_machine(payload))

    @route.get("{machine_id}/")
    def get_machine(self, machine_id: UUID):
        return {"message": "Details of machine"}

    @route.patch("{machine_id}/")
    def update_machine(self, machine_id: UUID):
        return {"message": "Machine updated"}

    @route.delete("{machine_id}/")
    def delete_machine(self, machine_id: UUID):
        return {"message": "Machine deleted"}

    @route.post("{machine_id}/token/")
    def issue_token(self, machine_id: UUID):
        return {"message": "Token generated for machine"}

    @route.post("{machine_id}/token/revoke/")
    def revoke_token(self, machine_id: UUID):
        return {"message": "Token revoked for machine"}

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
