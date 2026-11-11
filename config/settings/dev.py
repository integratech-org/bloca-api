from .base import *  # noqa: F403
from .base import INSTALLED_APPS

DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104

INSTALLED_APPS = [*INSTALLED_APPS, "django_extensions"]
