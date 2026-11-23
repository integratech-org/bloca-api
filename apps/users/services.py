from allauth.account.models import EmailAddress
from django.db import transaction
from rolepermissions.roles import assign_role

from apps.users.schemas import UserCreateIn  # noqa: TC001

from .models import User
from .tasks import send_verification_email


class UsersService:
    @transaction.atomic
    def create_user(self, payload: UserCreateIn) -> User:
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
