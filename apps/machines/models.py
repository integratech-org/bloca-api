import uuid

from django.db import models

# Create your models here.


class Machine(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(max_length=100, unique=True)
    token_hash = models.CharField(max_length=64, unique=True, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
