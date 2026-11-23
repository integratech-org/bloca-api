from django.utils import timezone
from factory.declarations import LazyFunction
from factory.declarations import Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = User

    username = Sequence(lambda n: f"user{n}@example.com")
    email = Sequence(lambda n: f"user{n}@example.com")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    date_joined = LazyFunction(timezone.now)
