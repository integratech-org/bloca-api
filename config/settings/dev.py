from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import env

DEBUG = True

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

INSTALLED_APPS = [*INSTALLED_APPS, "django_extensions"]
