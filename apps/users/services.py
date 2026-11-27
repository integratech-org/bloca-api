from allauth.account.models import EmailAddress
from django.db import IntegrityError
from django.db import transaction
from django.shortcuts import get_object_or_404
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

    def get_user(self, user_id: int) -> User:
        return get_object_or_404(User, id=user_id)

    def disable_user(self, user_id: int) -> None:
        user = get_object_or_404(User, id=user_id)
        user.is_active = False
        user.save(update_fields=["is_active", "updated_at"])

    def enable_user(self, user_id: int) -> None:
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save(update_fields=["is_active", "updated_at"])

    def delete_user(self, user_id: int) -> None:
        get_object_or_404(User, id=user_id).delete()

    def restore_user(self, user_id: int) -> None:
        user = get_object_or_404(User.objects.deleted_set(), id=user_id)
        try:
            with transaction.atomic():
                user.undelete()
        except IntegrityError:
            raise HttpError(409, "User email already in use") from None

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
