from ninja import Schema
from ninja_extra import api_controller, http_get, http_post
from ninja.responses import Response

from config import client


class PublishIn(Schema):
    topic: str
    msg: str


@api_controller("/example")
class ExampleController:
    @http_get("/hello")
    def hello(self):
        """
        Hello World endpoint
        """
        return {"message": "Hello World!"}

    @http_post("/publish")
    def publish(self, data: PublishIn):
        # Check if the client is connected
        if not client.is_connected():
            return Response({"error": "MQTT client is not connected"}, status=503)

        info = client.publish(data.topic, data.msg, qos=1)
        info.wait_for_publish(timeout=5)
        return {"code": info.rc}
