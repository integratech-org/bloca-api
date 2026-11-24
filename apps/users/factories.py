from django.utils import timezone
from factory.declarations import LazyFunction
from factory.django import DjangoModelFactory
from factory.faker import Faker

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        model = User

    username = Faker("user_name")
    email = Faker("email", domain="gmail.com")
    avatar_url = Faker("image_url")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    phone_number = Faker("numerify", text="(+63)9#########")
    address_line = Faker("street_address")
    barangay = Faker("city")
    city_municipality = Faker("city")
    province = Faker("state")
    date_joined = LazyFunction(timezone.now)
