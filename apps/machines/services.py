import asyncio
import json
import secrets
from collections.abc import AsyncGenerator  # noqa: TC003
from uuid import UUID  # noqa: TC003

from channels.layers import get_channel_layer
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.common.utils import hash_token
from apps.machines.filters import MachineFilterSchema  # noqa: TC001

from .models import Machine
from .schemas import MachineCreateIn  # noqa: TC001
from .schemas import MachineUpdateIn  # noqa: TC001


class MachineService:
    def list_machines(self, filters: MachineFilterSchema | None):
        machines = Machine.objects.all_with_deleted()
        if filters:
            return filters.filter(machines)
        return machines.filter(deleted_at__isnull=True)

    @transaction.atomic
    def create_machine(self, payload: MachineCreateIn) -> Machine:
        machine = Machine.objects.create(**payload.dict())
        token = self.issue_token(machine.id)
        machine.token = token  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]
        return machine

    def get_machine(self, machine_id: UUID) -> Machine:
        return get_object_or_404(Machine, id=machine_id)

    def update_machine(self, machine_id: UUID, payload: MachineUpdateIn) -> Machine:
        machine = get_object_or_404(Machine, id=machine_id)
        for attr, value in payload.dict().items():
            setattr(machine, attr, value)
        machine.save(update_fields=["name", "site", "updated_at"])
        return machine

    def delete_machine(self, machine_id: UUID):
        get_object_or_404(Machine, id=machine_id).delete()

    def issue_token(self, machine_id: UUID) -> str:
        machine = get_object_or_404(Machine, id=machine_id)
        token = secrets.token_urlsafe(32)
        machine.token_hash = hash_token(token)
        machine.revoked_at = None
        machine.save(update_fields=["token_hash", "revoked_at", "updated_at"])
        return token

    def revoke_token(self, machine_id: UUID) -> None:
        machine = get_object_or_404(Machine, id=machine_id)
        machine.token_hash = None
        machine.revoked_at = timezone.now()
        machine.save(update_fields=["token_hash", "revoked_at", "updated_at"])

    async def stream_events(self, machine_id: UUID) -> AsyncGenerator[str]:
        layer = get_channel_layer()
        assert layer is not None, "CHANNEL_LAYERS is not configured"
        channel = await layer.new_channel()
        group_name = f"machine_{machine_id}"
        await layer.group_add(group_name, channel)

        try:
            yield ": connected\n\n"
            while True:
                try:
                    event = await asyncio.wait_for(layer.receive(channel), timeout=30)
                except TimeoutError:
                    yield ": keep-alive\n\n"
                    continue

                yield f"data: {json.dumps(event['message'])}\n\n"
        finally:
            await layer.group_discard(group_name, channel)
