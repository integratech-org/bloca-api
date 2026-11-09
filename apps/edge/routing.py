from django.urls import path

from apps.machines.middleware import MachineTokenAuthMiddleware

from .consumers import EdgeConsumer

websocket_urlpatterns = [
    path("ws/edge/", MachineTokenAuthMiddleware(EdgeConsumer.as_asgi())),  # pyright: ignore[reportCallIssue, reportArgumentType]
]
