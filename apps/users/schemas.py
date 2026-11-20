from ninja import ModelSchema
from ninja import Schema
from pydantic import Field

from .models import User


class UserCreateIn(Schema):
    email: str = Field(description="User's email address")
    first_name: str = Field(min_length=1, max_length=150, description="First name")
    last_name: str = Field(min_length=1, max_length=150, description="Last name")
    role: str = Field(description="User role: Admin or Operator")


class UserOut(ModelSchema):
    role: str = Field(description="User's assigned role")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]
