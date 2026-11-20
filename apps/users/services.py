from typing import TYPE_CHECKING

from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmationHMAC
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
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
        user = User.objects.create_user(
            username=payload.email,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            is_active=True,
        )
        user.set_password(payload.last_name)  # temporary, see note below
        user.save()

        email_address = EmailAddress.objects.create(
            user=user,
            email=payload.email,
            verified=False,
            primary=True,
        )

        assign_role(user, self._get_role_class(payload.role))

        self._send_verification_email(user, email_address)

        return user, payload.role

    def _send_verification_email(self, user: User, email_address: EmailAddress):
        """Send email verification with both text and HTML versions"""

        # Generate confirmation key
        confirmation = EmailConfirmationHMAC(email_address)
        activate_url = f"{settings.FRONTEND_URL}/verify?key={confirmation.key}"

        # Render templates
        subject = render_to_string(
            "account/email/email_confirmation_subject.txt",
            {
                "user": user,
            },
        ).strip()

        text_content = render_to_string(
            "account/email/email_confirmation_message.txt",
            {
                "user": user,
                "activate_url": activate_url,
            },
        )

        html_content = render_to_string(
            "account/email/email_confirmation_message.html",
            {
                "user": user,
                "activate_url": activate_url,
            },
        )

        # Send email with both versions
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
