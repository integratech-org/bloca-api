from allauth.account.models import EmailAddress
from django.db import transaction
from ninja.errors import HttpError
from rolepermissions.roles import assign_role

from .filters import UserFilterSchema  # noqa: TC001
from .models import User
from .schemas import UserCreateIn  # noqa: TC001
from .tasks import send_verification_email


class UsersService:
    def list_users(self, filters: UserFilterSchema | None):
        users = User.objects.all_with_deleted()  # pyright: ignore[reportAttributeAccessIssue]
        if filters:
            return filters.filter(users)
        return users.filter(deleted_at__isnull=True)

    @transaction.atomic
    def create_user(self, payload: UserCreateIn) -> User:
        if User.objects.all_with_deleted().filter(email__iexact=payload.email).exists():  # pyright: ignore[reportAttributeAccessIssue]
            raise HttpError(409, "User with this email already exists.")

        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            password=payload.last_name,
        )

        email_address = EmailAddress.objects.create(
            user=user,
            email=payload.email,
            verified=False,
            primary=True,
        )

        assign_role(user, payload.role)

        transaction.on_commit(lambda: send_verification_email.delay(email_address.pk))

        return user
