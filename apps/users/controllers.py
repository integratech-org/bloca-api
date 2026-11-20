from injector import inject
from ninja.responses import Status
from ninja_extra import api_controller
from ninja_extra import route

from .schemas import UserCreateIn
from .schemas import UserOut
from .services import UsersService  # noqa: TC001


@api_controller("/users", tags=["Users"])
class UsersController:
    @inject
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @route.post("", response={201: UserOut})
    def create_user(self, payload: UserCreateIn):
        """
        Create a new user account.

        A verification email will be sent to the user's email address.
        """
        user, role = self.users_service.create_user(payload)

        return Status(
            201,
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "date_joined": user.date_joined,
                "role": role,
            },
        )
