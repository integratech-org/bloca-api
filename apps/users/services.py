from typing import TYPE_CHECKING

from allauth.account.models import EmailAddress
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
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
        Create a new user account and send password setup email.

        Returns:
            tuple[User, str]: Created user and their assigned role
        """
        # Create user with email as username (no password)
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            is_active=True,  # Set to True so password reset works
        )

        # Mark email as verified since admin created it
        EmailAddress.objects.create(
            user=user, email=payload.email, verified=True, primary=True
        )

        # Assign role
        role_class = self._get_role_class(payload.role)
        assign_role(user, role_class)

        # Send password setup email
        self._send_password_setup_email(user)

        return user, payload.role

    def _send_password_setup_email(self, user: User):
        """Send email with password setup link"""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # TODO: Update URL to match frontend password reset page
        reset_url = f"http://localhost:3000/auth/reset-password?uid={uid}&token={token}"

        subject = "Set up your BLOCA account"
        message = f"""
        Hi {user.first_name},

        Your BLOCA account has been created. Please set up your password by
        clicking the link below:

        {reset_url}

        If you didn't request this account, please ignore this email.

        Best regards,
        The BLOCA Team
                """

        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[user.email],
            fail_silently=False,
        )
