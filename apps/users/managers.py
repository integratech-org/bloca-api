from django.contrib.auth.models import UserManager
from softdelete.models import SoftDeleteManager


class CustomUserManager(SoftDeleteManager, UserManager):
    pass
