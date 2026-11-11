from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, blank=True)
    avatar_url = models.URLField(blank=True)

    address_line = models.CharField(max_length=255, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    city_municipality = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email
