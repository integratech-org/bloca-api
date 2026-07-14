from ninja_extra import NinjaExtraAPI
from apps.example.controllers import ExampleController

api = NinjaExtraAPI()

api.register_controllers(ExampleController)
