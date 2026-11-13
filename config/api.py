from ninja_extra import NinjaExtraAPI

from apps.machines.controllers import MachinesController

api = NinjaExtraAPI()

api.register_controllers(MachinesController)
