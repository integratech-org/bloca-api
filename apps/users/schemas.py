from enum import StrEnum

from ninja import ModelSchema
from ninja import Schema
from pydantic import EmailStr
from pydantic import Field

from .models import User


class RoleEnum(StrEnum):
    SYSTEM_ADMIN = "system_admin"
    ADMIN = "admin"
    OPERATOR = "operator"


class UserCreateIn(Schema):
    email: EmailStr = Field(min_length=1, max_length=254, description="Email address")
    first_name: str = Field(min_length=1, max_length=150, description="First name")
    last_name: str = Field(min_length=1, max_length=150, description="Last name")
    role: RoleEnum = Field(description="Role of the user")


class UserCreateOut(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
