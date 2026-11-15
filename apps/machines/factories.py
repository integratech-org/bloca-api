from django.utils import timezone
from factory.declarations import LazyAttribute
from factory.declarations import LazyFunction
from factory.declarations import Sequence
from factory.django import DjangoModelFactory
from factory.faker import Faker

from apps.common.utils import hash_token

from .models import Machine


class MachineFactory(DjangoModelFactory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = Machine

    name = Sequence(lambda n: f"BLOCA-machine{n}")
    site = Faker("city")
    token_hash = LazyAttribute(lambda o: hash_token(o.name))
    created_at = LazyFunction(timezone.now)
    updated_at = LazyFunction(timezone.now)
