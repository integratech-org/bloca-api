from ninja import ModelSchema
from ninja import Schema
from pydantic import Field

from .models import Machine


class MachinesCreateIn(Schema):
    name: str = Field(min_length=1, max_length=100, description="Name of the machine")
    site: str = Field(default="", max_length=100, description="Site of the machine")


class MachinesCreateOut(ModelSchema):
    token: str = Field(description="Token for the machine")

    class Meta:
        model = Machine
        fields = [
            "id",
            "name",
            "site",
        ]
