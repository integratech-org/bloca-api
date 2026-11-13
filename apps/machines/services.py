import hashlib
import secrets
from uuid import UUID  # noqa: TC003

from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Machine
from .schemas import MachinesCreateIn  # noqa: TC001


class MachinesService:
    def hash_token(self, token: str) -> str:
        return hashlib.sha256(str(token).encode("utf-8")).hexdigest()

    def authenticate(self, token: str) -> Machine | None:
        if not token:
            return None
        return Machine.objects.filter(token_hash=self.hash_token(token)).first()

    def issue_token(self, machine_id: UUID) -> str:
        machine = get_object_or_404(Machine, id=machine_id)
        token = secrets.token_urlsafe(32)
        machine.token_hash = self.hash_token(token)
        machine.save(update_fields=["token_hash"])
        return token

    def revoke_token(self, machine_id: UUID) -> None:
        machine = get_object_or_404(Machine, id=machine_id)
        machine.token_hash = None
        machine.save(update_fields=["token_hash", "updated_at"])

    @transaction.atomic
    def create_machine(self, payload: MachinesCreateIn) -> tuple[Machine, str]:
        machine = Machine.objects.create(**payload.dict())
        token = self.issue_token(machine.id)
        return machine, token
