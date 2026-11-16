import uuid

from django.db import models

from apps.common.models import BaseModel


class Machine(BaseModel):
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

    class Meta(BaseModel.Meta):
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

    def __str__(self):
        return self.name
