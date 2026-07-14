from ninja_extra import api_controller, http_get


@api_controller("/example")
class ExampleController:
    @http_get("/hello")
    def hello(self):
        """
        Hello World endpoint
        """
        return {"message": "Hello World!"}
