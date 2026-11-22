from ninja import ModelSchema
from ninja import Schema
from pydantic import Field

from .models import User


class UserCreateIn(Schema):
    email: str = Field(description="User's email address")
    first_name: str = Field(min_length=1, max_length=150, description="First name")
    last_name: str = Field(min_length=1, max_length=150, description="Last name")
    role: str = Field(description="Role to assign: Admin or Operator")


class UserCreateOut(ModelSchema):
    role: str = Field(description="Assigned role: Admin or Operator")

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
