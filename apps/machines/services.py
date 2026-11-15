import asyncio
import hashlib
import json
import secrets
from collections.abc import AsyncGenerator  # noqa: TC003
from uuid import UUID  # noqa: TC003

from channels.layers import get_channel_layer
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
    def create_machine(self, payload: MachinesCreateIn) -> Machine:
        machine = Machine.objects.create(**payload.dict())
        token = self.issue_token(machine.id)
        machine.token = token  # type: ignore[attr-defined]  # pyright: ignore[reportAttributeAccessIssue]
        return machine

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
