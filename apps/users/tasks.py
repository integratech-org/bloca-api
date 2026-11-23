from allauth.account.models import EmailAddress
from celery import shared_task


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def send_verification_email(email_address_id: int) -> None:
    try:
        email_address = EmailAddress.objects.select_related("user").get(
            pk=email_address_id
        )
    except EmailAddress.DoesNotExist:
        return

    if email_address.verified:
        return

    email_address.send_confirmation(request=None, signup=False)
