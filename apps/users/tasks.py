from allauth.account.models import EmailAddress
from allauth.account.models import EmailConfirmationHMAC
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.users.models import User


@shared_task(bind=True, max_retries=3, retry_backoff=True)
def send_verification_email_task(self, user_id: int, email_address_id: int):
    """
    Send email verification link to user.

    Retries: 3 attempts with exponential backoff (1min, 5min, 25min)
    """
    try:
        user = User.objects.get(id=user_id)
        email_address = EmailAddress.objects.get(id=email_address_id)

        # Generate confirmation key
        confirmation = EmailConfirmationHMAC(email_address)
        activate_url = f"{settings.FRONTEND_URL}/verify?key={confirmation.key}"

        # Render templates
        subject = render_to_string(
            "account/email/email_confirmation_subject.txt",
            context={"user": user},
        ).strip()

        text_content = render_to_string(
            "account/email/email_confirmation_message.txt",
            context={"user": user, "activate_url": activate_url},
        )

        html_content = render_to_string(
            "account/email/email_confirmation_message.html",
            context={"user": user, "activate_url": activate_url},
        )

        # Send email
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except (User.DoesNotExist, EmailAddress.DoesNotExist, Exception) as exc:
        # Retry with exponential backoff: 1min, 5min, 25min
        raise self.retry(exc=exc, countdown=60 * (5**self.request.retries)) from exc
