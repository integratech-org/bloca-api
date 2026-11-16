from django.db import models
from softdelete.models import SoftDeleteObject


class BaseModel(SoftDeleteObject, models.Model):  # type: ignore[django-manager-missing]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(SoftDeleteObject.Meta):
        abstract = True
