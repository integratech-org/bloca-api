from injector import inject
from ninja import Query  # noqa: TC002
from ninja.responses import Status
from ninja_extra import api_controller
from ninja_extra import paginate
from ninja_extra import route
from ninja_extra.ordering import Ordering
from ninja_extra.ordering import ordering
from ninja_extra.pagination import PageNumberPaginationExtra
from ninja_extra.pagination import PaginatedResponseSchema
from ninja_extra.searching import Searching
from ninja_extra.searching import searching

from .filters import UserFilterSchema  # noqa: TC001
from .schemas import UserCreateIn
from .schemas import UserCreateOut
from .schemas import UserOut
from .services import UsersService  # noqa: TC001


@api_controller("/users", tags=["Users"])
class UsersController:
    @inject
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @route.get("/", response=PaginatedResponseSchema[UserOut])
    @paginate(PageNumberPaginationExtra, page_size=25)
    @ordering(
        Ordering,
        ordering_fields=["email", "first_name", "last_name", "date_joined"],
    )
    @searching(
        Searching, search_fields=["email", "first_name", "last_name", "username"]
    )
    def get_users(self, filters: Query[UserFilterSchema]):
        return self.users_service.list_users(filters)

    @route.get("/{user_id}/", response={200: UserOut})
    def get_user(self, user_id: int):
        return self.users_service.get_user(user_id)

    @route.post("/{user_id}/disable/", response={204: None})
    def disable_user(self, user_id: int):
        self.users_service.disable_user(user_id)
        return Status(204, None)

    @route.post("/{user_id}/enable/", response={204: None})
    def enable_user(self, user_id: int):
        self.users_service.enable_user(user_id)
        return Status(204, None)

    @route.post("/", response={201: UserCreateOut})
    def create_user(self, payload: UserCreateIn):
        user = self.users_service.create_user(payload)
        return Status(201, user)
