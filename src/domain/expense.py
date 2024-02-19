from pydantic import Field
from src.application.custom_base_model import CustomBaseModel
from src.domain import common


class CreateExpense(CustomBaseModel):
    name: str


class GetExpense(CustomBaseModel):
    id: common.ObjectID
    name: str