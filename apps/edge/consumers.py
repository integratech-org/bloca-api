from channels.generic.websocket import AsyncJsonWebsocketConsumer
from pydantic import ValidationError

from .messages import TelemetryMessage


class EdgeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.machine = self.scope["machine"]  # pyright: ignore[reportGeneralTypeIssues]
        self.group_name = f"machine_{self.machine.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get("type") == "telemetry":
            try:
                msg = TelemetryMessage.model_validate(content)
            except ValidationError as exc:
                await self.send_json({"error": exc.errors()})
                return

            await self.channel_layer.group_send(
                self.group_name,
                {"type": "machine.telemetry", "message": msg.model_dump()},
            )

    async def machine_telemetry(self, event):
        pass
