from typing import TYPE_CHECKING

from allauth.account.models import EmailAddress
from django.db import transaction
from rolepermissions.roles import assign_role

from config.roles import Admin
from config.roles import Operator

from .models import User
from .tasks import send_verification_email_task

if TYPE_CHECKING:
    from .schemas import UserCreateIn


class UsersService:
    @transaction.atomic
    def create_user(self, payload: UserCreateIn) -> User:
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )
        user.set_password(payload.last_name)  # temporary, see note below
        user.save()

        email_address = EmailAddress.objects.create(
            user=user,
            email=payload.email,
            verified=False,
            primary=True,
        )

        assign_role(user, Admin if payload.role == "Admin" else Operator)

        user.role = payload.role  # type: ignore[attr-defined]

        send_verification_email_task.delay(user.id, email_address.id)

        return user
