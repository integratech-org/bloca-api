from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.security.websocket import WebsocketDenier

from apps.common.utils import hash_token

from .models import Machine


@database_sync_to_async
def _authenticate(token: str) -> Machine | None:
    if not token:
        return None
    return Machine.objects.filter(token_hash=hash_token(token)).first()


class MachineTokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):  # pyright: ignore[reportIncompatibleMethodOverride]
        machine = None

        headers = dict(scope.get("headers", []))
        auth = headers.get(b"authorization", b"").decode()
        scheme, _, raw = auth.partition(" ")
        if scheme.lower() == "bearer" and raw.strip():
            machine = await _authenticate(raw.strip())

        if machine is None:
            return await WebsocketDenier()(scope, receive, send)

        scope = dict(scope, machine=machine)
        return await super().__call__(scope, receive, send)
