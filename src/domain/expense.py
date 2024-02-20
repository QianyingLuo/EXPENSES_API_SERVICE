from src.application.custom_base_model import CustomBaseModel
from src.domain import common

class CreateExpense(CustomBaseModel):
    name: str


class GetExpense(CustomBaseModel):
    id: common.ObjectID
    name: str

class UserExpense(CustomBaseModel):
    name: str
    user: common.ObjectID
    quantity: float
    datetime: common.AwareDatetime
