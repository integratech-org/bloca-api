from ninja_extra import NinjaExtraAPI

from apps.machines.controllers import MachineController

api = NinjaExtraAPI()

api.register_controllers(MachineController)
