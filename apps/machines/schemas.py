from ninja import ModelSchema
from ninja import Schema
from pydantic import Field

from .models import Machine


class MachineOut(ModelSchema):
    token_status: str = Field(description="Status of the machine token")

    class Meta:
        model = Machine
        fields = ["id", "name", "site", "created_at", "updated_at", "deleted_at"]


class MachineCreateIn(Schema):
    name: str = Field(min_length=1, max_length=100, description="Name of the machine")
    site: str = Field(default="", max_length=100, description="Site of the machine")


class MachineCreateOut(ModelSchema):
    token: str = Field(description="Token for the machine")

    class Meta:
        model = Machine
        fields = [
            "id",
            "name",
            "site",
        ]


class MachineUpdateIn(Schema):
    name: str = Field(min_length=1, max_length=100, description="Name of the machine")
    site: str = Field(default="", max_length=100, description="Site of the machine")


class MachineUpdateOut(ModelSchema):
    class Meta:
        model = Machine
        fields = [
            "id",
            "name",
            "site",
        ]


class MachineIssueTokenOut(Schema):
    token: str = Field(description="Token for the machine")
