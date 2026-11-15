import asyncio
import json
import secrets
from collections.abc import AsyncGenerator  # noqa: TC003
from uuid import UUID  # noqa: TC003

from channels.layers import get_channel_layer
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.common.utils import hash_token

from .models import Machine
from .schemas import MachinesCreateIn  # noqa: TC001
from .schemas import MachinesUpdateIn  # noqa: TC001


class MachinesService:
    def list_machines(self):
        return Machine.objects.all()

    @transaction.atomic
    def create_machine(self, payload: MachinesCreateIn) -> Machine:
        machine = Machine.objects.create(**payload.dict())
        token = self.issue_token(machine.id)
        machine.token = token  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]
        return machine

    def get_machine(self, machine_id: UUID) -> Machine:
        return get_object_or_404(Machine, id=machine_id)

    def update_machine(self, machine_id: UUID, payload: MachinesUpdateIn) -> Machine:
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
        machine.save(update_fields=["token_hash"])
        return token

    def revoke_token(self, machine_id: UUID) -> None:
        machine = get_object_or_404(Machine, id=machine_id)
        machine.token_hash = None
        machine.save(update_fields=["token_hash", "updated_at"])

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
