from uuid import UUID  # noqa: TC003

from injector import inject
from ninja.responses import Status
from ninja_extra import api_controller
from ninja_extra import route

from .schemas import MachinesCreateIn
from .schemas import MachinesCreateOut
from .services import MachinesService  # noqa: TC001


@api_controller("/machines", tags=["Machines"])
class MachinesController:
    @inject
    def __init__(self, machines_service: MachinesService):
        self.machines_service = machines_service

    @route.get("")
    def get_machines(self):
        return {"message": "List of machines"}

    @route.post("", response={201: MachinesCreateOut})
    def create_machine(self, payload: MachinesCreateIn):
        machine, token = self.machines_service.create_machine(payload)
        return Status(
            201,
            {
                "id": machine.id,
                "name": machine.name,
                "site": machine.site,
                "token": token,
            },
        )

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
    def generate_token(self, machine_id: UUID):
        return {"message": "Token generated for machine"}

    @route.post("{machine_id}/token/revoke/")
    def revoke_token(self, machine_id: UUID):
        return {"message": "Token revoked for machine"}
