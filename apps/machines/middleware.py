from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.security.websocket import WebsocketDenier

from apps.machines.services import MachineService


class MachineTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        machine = None

        headers = dict(scope.get("headers", []))
        auth = headers.get(b"authorization", b"").decode()
        scheme, _, raw = auth.partition(" ")
        if scheme.lower() == "bearer" and raw.strip():
            machine = await database_sync_to_async(MachineService.authenticate)(
                raw.strip()
            )

        if machine is None:
            return await WebsocketDenier()(scope, receive, send)

        scope = dict(scope, machine=machine)
        return await super().__call__(scope, receive, send)
