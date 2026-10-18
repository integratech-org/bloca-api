from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]  # noqa: RUF012

    def __str__(self):
        return self.email
