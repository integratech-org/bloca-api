import uuid

from django.db import models

from apps.common.models import BaseModel


class Machine(BaseModel):
    class TokenStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        REVOKED = "revoked", "Revoked"
        NOT_ISSUED = "not_issued", "Not Issued"

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=100, unique=True)
    site = models.CharField(max_length=100, blank=True)
    token_hash = models.CharField(
        max_length=64, unique=True, editable=False, blank=True, null=True
    )
    revoked_at = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta(BaseModel.Meta):
        permissions = [
            ("restore_machine", "Can restore deleted machine"),
            ("issue_machine_token", "Can issue machine token"),
            ("revoke_machine_token", "Can revoke machine token"),
            ("stream_machine", "Can stream machine events"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                condition=models.Q(deleted_at__isnull=True),
                name="uniq_machine_name_alive",
            ),
            models.UniqueConstraint(
                fields=["token_hash"],
                condition=models.Q(deleted_at__isnull=True),
                name="uniq_machine_token_hash_alive",
            ),
        ]

    @property
    def token_status(self):
        if self.revoked_at:
            return self.TokenStatus.REVOKED
        if self.token_hash:
            return self.TokenStatus.ACTIVE
        return self.TokenStatus.NOT_ISSUED

    def __str__(self):
        return self.name
