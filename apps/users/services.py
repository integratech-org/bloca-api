from typing import TYPE_CHECKING

from django.db import transaction
from rolepermissions.roles import assign_role

from config.roles import Admin
from config.roles import Operator

from .models import User

if TYPE_CHECKING:
    from .schemas import UserCreateIn


class UsersService:
    def _get_role_class(self, role: str):
        """Map frontend role to backend role class"""
        role_mapping = {
            "Admin": Admin,
            "Operator": Operator,
        }
        return role_mapping.get(role, Operator)

    @transaction.atomic
    def create_user(self, payload: UserCreateIn) -> tuple[User, str]:
        """
        Create a new user account.

        Returns:
            tuple[User, str]: Created user and their assigned role
        """
        # Create user with email as username
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            is_active=False,
        )

        # Assign role
        role_class = self._get_role_class(payload.role)
        assign_role(user, role_class)

        return user, payload.role
