from ninja_extra import NinjaExtraAPI

from apps.machines.controllers import MachineController
from apps.users.controllers import UsersController

api = NinjaExtraAPI()

api.register_controllers(MachineController, UsersController)
