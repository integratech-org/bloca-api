from channels.generic.websocket import AsyncJsonWebsocketConsumer


class EdgeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json({"message": "Hello from EdgeConsumer!"})

    async def disconnect(self, code):
        pass
